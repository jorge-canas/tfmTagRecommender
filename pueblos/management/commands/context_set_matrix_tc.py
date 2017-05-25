#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from django.core.management.base import BaseCommand
from pueblos.SemanticMotor.ConfusionMatrix import ConfusionMatrix
from pueblos.common.util.utilities import clean_accents, get_list_words
from pueblos.SemanticMotor.SemanticMotor import SemanticMotor
from pueblos.models import PueblosNoticias, PueblosNoticiasTest, PueblosNoticiasTestCategorias, \
    PueblosDiccionarioSintactico


class Command(BaseCommand):
    """Use example:
     python manage.py test_context_set_matrix --test_file prueba_words_category.csv --output_file confusion_matrix"""
    help = 'Realiza el test del contexto creado y genera matrix de confusion'

    def add_arguments(self, parser):
        parser.add_argument('--output_file', dest='output_file', nargs='?', default='',
                            help='Nombre del fichero donde se guardara la matriz de confusion')
        parser.add_argument('--min_confidence', dest='min_confidence', nargs='?', type=float, default=0.55,
                            help='Confianza mínima que tiene que cumplir la regla para ser sugerida',
                            )
        parser.add_argument('--min_support', dest='min_support', nargs='?', type=float, default=0.1,
                            help='Porcentaje de soporte mínimo que tiene que cumplir la regla para ser sugerida',
                            )
        parser.add_argument('--use_syn_dict', action='store_true', dest='use_syn_dict', default=False,
                            help='Usar el diccionario sintactico para sustituir algunas palabras incorrectas')

    def handle(self, *args, **options):
        use_syn_dict = options['use_syn_dict']
        confidence = options['min_confidence']
        support = options['min_support']
        if confidence > 1.0:
            confidence = 1.0
        elif confidence < 0:
            confidence = 0.01

        if support > 1.0:
            support = 1.0
        elif support < 0:
            support = 0.01

        syn_dict = {}
        if use_syn_dict:
            self.stdout.write('Using dict')
            syntactic_dictionary = PueblosDiccionarioSintactico.objects.all()
            for sd in syntactic_dictionary:
                syn_dict[sd.word] = sd.replace_word
        n_stored = 0
        n_suggested = 0
        output = ''
        savefile = options['output_file'] + '.csv'
        results_file = savefile[:-4]
        sm = SemanticMotor()
        sm.save_semantic_motor(results_file + '-semantic_motor.txt')
        test_news = PueblosNoticiasTest.objects.all()
        news_results = {}
        labels = dict()
        with open(results_file + '-rules-track.txt', 'w') as fout:
            fout.write('')
        min_support = len(test_news) * support
        min_confidence = confidence
        for test_n in test_news:
            news_words = get_list_words(test_n.dscuerpo)

            if use_syn_dict:
                for index, word in enumerate(news_words):
                    if word in syn_dict:
                        if len(syn_dict[word]) >= 3:  # Check if there is a correct word
                            news_words[index] = syn_dict[word]

            results = sm.get_conclusion_names(news_words)
            suggested_categories = []
            rule_output = str(test_n.id) + '\n'
            for result in results:  # Testing purpose, estimate rule support
                category = result.category
                rule_output += category + ';'
                rule_output += result.rule.str_csv() + '\n'
            with open(results_file + '-rules-track.txt', 'a') as fout:
                rule_output += '--------------- Next News --------------------\n'
                fout.write(rule_output.encode('utf-8'))

            for result in results:
                category = result.category
                if category not in suggested_categories and (
                                    result.rule.get_confidence() >= min_confidence or
                                    result.rule.get_support() > min_support):
                    suggested_categories.append(category)

            if not suggested_categories and len(results) > 0:  # Get at least one category
                min_rule_confidence = results[0].rule.get_confidence()
                for result in results:
                    category = result.category
                    if result.rule.get_confidence() == min_rule_confidence and category not in suggested_categories:
                        suggested_categories.append(category)
                    else:
                        break

            for suggested_category in suggested_categories:
                news_suggested_category = PueblosNoticiasTestCategorias(
                    id=None, noticia_test=test_n, categorias_sugeridas=suggested_category)
                news_suggested_category.save()

            n = PueblosNoticias.objects.get(id=test_n.noticia_id)
            categories = n.get_categorias_string()
            clean_categories = []
            for category in categories:
                category = 'ETIQUETA_' + re.sub(ur'[ ]', '_', category.lower())
                category = clean_accents(category)
                clean_categories.append(category)
            news_results[test_n.noticia_id] = [clean_categories, suggested_categories]
        total_elements = 0.0
        correct_result = 0.0
        for n, list_categories in news_results.items():
            stored_categories, suggested_categories = list_categories
            n_stored += len(stored_categories)
            n_suggested += len(suggested_categories)
            if sm.check_correct(stored_categories, suggested_categories):
                result_text = ' Contiene las etiquetas'
                correct_result += 1.0
            else:
                result_text = ' No contiene las etiquetas'
            total_elements += 1.0
            output += 'id ' + str(n) + ';stored ' + str(stored_categories) + ';suggested' \
                      + str(suggested_categories) + result_text + '\n'
        with open(results_file + '-results-track.txt', 'w') as fout:
            fout.write(output.encode('utf-8'))
        output_result = ''
        output_result += 'Total number of stored categories ' + str(n_stored) + '\n'
        output_result += 'Total number of suggested categories ' + str(n_suggested) + '\n'
        output_result += 'Total number of element check ' + str(total_elements) + '\n'
        output_result += 'Total number of correct element ' + str(correct_result) + '\n'
        output_result += 'Correct percentage ' + str(correct_result / total_elements * 100.0) + '%\n'
        with open(results_file + '-results.txt', 'w') as fout:
            fout.write(output_result.encode('utf-8'))
        self.stdout.write('Finished')
