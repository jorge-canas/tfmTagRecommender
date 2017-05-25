#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from django.core.management.base import BaseCommand
from pueblos.SemanticMotor.ConfusionMatrix import ConfusionMatrix
from pueblos.common.util.utilities import clean_accents, get_list_words
from pueblos.SemanticMotor.SemanticMotor import SemanticMotor
from pueblos.models import PueblosNoticias, PueblosDiccionarioSintactico, PueblosCategoriasSemandal, \
    PueblosNoticiaCategorizada


class Command(BaseCommand):
    """Use example:
     python manage.py suggest_category_news 1 --min_confidence 0.4 --min_support 40
     """
    help = 'Devuelve una sugerencia de etiquetas'

    def add_arguments(self, parser):
        parser.add_argument('news_id', type=int, nargs='?', help='Id de la noticia')
        parser.add_argument('--min_confidence', dest='min_confidence', nargs='?', type=float, default=0.4,
                            help='Confianza mínima que tiene que cumplir la regla para ser sugerida',
                            )
        parser.add_argument('--min_support', dest='min_support', nargs='?', type=int, default=40,
                            help='Porcentaje de soporte mínimo que tiene que cumplir la regla para ser sugerida',
                            )

    def handle(self, *args, **options):
        news_id = options['news_id']
        if news_id and news_id >= 1:
            confidence = options['min_confidence']
            support = options['min_support']
            if confidence > 1.0:
                confidence = 1.0
            elif confidence < 0:
                confidence = 0.01

            if support <= 0:
                support = 1
            db_categories = PueblosCategoriasSemandal.objects.all()
            db_category_id = {}
            for db_category in db_categories:
                category = db_category.dscategoria
                index = 'ETIQUETA_' + re.sub(ur'[ ]', '_', category.lower())
                index = clean_accents(index)
                db_category_id[index] = db_category.id

            sm = SemanticMotor()
            min_support = support
            min_confidence = confidence
            news = PueblosNoticias.objects.get(pk=news_id)
            if news.dscuerpo:  # some news does not have a body (dscuerpo)
                text = news.dstitular + ' ' + news.dscuerpo
            else:
                text = news.dstitular
            news_words = get_list_words(text)
            results = sm.get_conclusion_names(news_words)
            """
            output = ''
            for word in news_words:
                output += ', ' + word
            self.stdout.write(output)
            """
            suggested_categories = []

            for result in results:
                category = result.category
                if category not in suggested_categories and (
                                    result.rule.get_confidence() >= min_confidence or
                                    result.rule.get_support() >= min_support):
                    suggested_categories.append(category)

            # Get at least best confidence and support categories
            min_rule_confidence = results[0].rule.get_confidence()
            for result in results:
                category = result.category
                if result.rule.get_confidence() == min_rule_confidence and category not in suggested_categories:
                    suggested_categories.append(category)
                else:
                    break
            results.sort(key=lambda x: x.rule.get_support(), reverse=True)
            min_rule_support = results[0].rule.get_support()
            for result in results:
                category = result.category
                if result.rule.get_support() == min_rule_support and category not in suggested_categories:
                    suggested_categories.append(category)
                else:
                    break

            clean_categories = []
            for suggested_category in suggested_categories:
                tag = db_category_id[suggested_category]

                if tag != 33 and tag != 17:  # 33 = id for Ayuntamiento, 17 = id for Generales
                    clean_categories.append(db_category_id[suggested_category])

                # clean_categories.append(db_category_id[suggested_category])
            for category_id in clean_categories:
                category_town = PueblosNoticiaCategorizada(
                    id=None, noticia_id=news_id, categorias_sugeridas_id=category_id)
                category_town.save()

            """
            output = str(news_id) + ' '
            if clean_categories:
                output += str(clean_categories.pop(0))
                for id in clean_categories:
                    output += ', ' + str(id)
            """
            return self.stdout.write('Finished para noticia con id ' + str(news_id))
        else:
            return self.stderr.write('Error - No se ha proporcionado un id o no es valido')
