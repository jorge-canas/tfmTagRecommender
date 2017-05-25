#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from django.core.management.base import BaseCommand
from pueblos.SemanticMotor.ConfusionMatrix import ConfusionMatrix
from pueblos.common.util.utilities import clean_accents, get_list_words
from pueblos.SemanticMotor.SemanticMotor import SemanticMotor
from pueblos.models import PueblosNoticias, PueblosDiccionarioSintactico, PueblosCategoriasSemandal


class Command(BaseCommand):
    """Use example:
     python manage.py recommend_tags --news_body "News text to check recommendations"
     """
    help = 'Devuelve una sugerencia de etiquetas'

    def add_arguments(self, parser):
        parser.add_argument('--news_body', dest='news_body', nargs='?', default='',
                            help='Texto del cuerpo de la noticia')
        parser.add_argument('--use_syn_dict', action='store_true', dest='use_syn_dict', default=False,
                            help='Usar el diccionario sintactico para sustituir algunas palabras incorrectas')
        parser.add_argument('--min_confidence', dest='min_confidence', nargs='?', type=float, default=0.4,
                            help='Confianza mínima que tiene que cumplir la regla para ser sugerida',
                            )
        parser.add_argument('--min_support', dest='min_support', nargs='?', type=int, default=40,
                            help='Porcentaje de soporte mínimo que tiene que cumplir la regla para ser sugerida',
                            )

    def handle(self, *args, **options):
        news_body = options['news_body']
        # self.stdout.write(news_body)
        # self.stdout.write(str(options['min_confidence']))
        # self.stdout.write(str(options['min_support']))
        if len(news_body) >= 50:
            confidence = options['min_confidence']
            support = options['min_support']
            if confidence > 1.0:
                confidence = 1.0
            elif confidence < 0:
                confidence = 0.01

            if support <= 0:
                support = 1

            use_syn_dict = options['use_syn_dict']

            syn_dict = {}
            if use_syn_dict:
                # self.stdout.write('Using dict')
                syntactic_dictionary = PueblosDiccionarioSintactico.objects.all()
                for sd in syntactic_dictionary:
                    syn_dict[sd.word] = sd.replace_word
            db_categories = PueblosCategoriasSemandal.objects.all()
            db_category_names = {}
            for db_category in db_categories:
                category = db_category.dscategoria
                index = 'ETIQUETA_' + re.sub(ur'[ ]', '_', category.lower())
                index = clean_accents(index)
                db_category_names[index] = category

            sm = SemanticMotor()
            min_support = support
            min_confidence = confidence
            news_words = get_list_words(news_body)
            if use_syn_dict:
                for index, word in enumerate(news_words):
                    if word in syn_dict:
                        if len(syn_dict[word]) >= 3:  # Check if there is a correct word
                            news_words[index] = syn_dict[word]
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
                print result
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
                tag = db_category_names[suggested_category]
                if tag != 'Ayuntamiento' and tag != 'Generales':
                    clean_categories.append(tag)
            output = ''
            if clean_categories:
                output = clean_categories.pop(0)
                for word in clean_categories:
                    output += ', ' + word
            return self.stdout.write(output)
        else:
            return self.stderr.write('El tamaño del texto tiene que ser mayor a 50 caracteres')


