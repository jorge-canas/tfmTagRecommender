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
        parser.add_argument('--use_syn_dict', action='store_true', dest='use_syn_dict', default=False,
                            help='Usar el diccionario sintactico para sustituir algunas palabras incorrectas')

    def handle(self, *args, **options):
        n_stored = 0
        n_suggested = 0
        use_syn_dict = options['use_syn_dict']
        syn_dict = {}
        if use_syn_dict:
            self.stdout.write('Context set matrix - Using dict')
            syntactic_dictionary = PueblosDiccionarioSintactico.objects.all()
            for sd in syntactic_dictionary:
                syn_dict[sd.word] = sd.replace_word
        output = ''
        output_file = options['output_file']
        savefile = 'files/confusion_matrix.csv'

        if output_file:
            if 'files_batch/' in output_file:
                savefile = output_file
            elif 'files/' not in output_file:
                savefile = 'files/' + output_file

            if '.csv' not in savefile:
                savefile = output_file + '.csv'
        results_file = savefile[:-4]
        sm = SemanticMotor()
        sm.save_semantic_motor(results_file + '-semantic_motor.txt')
        test_news = PueblosNoticiasTest.objects.all()
        news_results = {}
        # labels = dict()
        with open(results_file + '-rules-track.txt', 'w') as fout:
            fout.write('')

        min_confidence = 0.70
        min_support = len(test_news) * 0.50
        min_support_with_confidence = len(test_news) * 0.30
        min_confidence_with_support = 0.50
        for test_n in test_news:
            news_words = get_list_words(test_n.dscuerpo)

            if use_syn_dict:
                for index, word in enumerate(news_words):
                    if word in syn_dict:
                        if len(syn_dict[word]) >= 3:  # Check if there is a correct word
                            news_words[index] = syn_dict[word]

            results = sm.get_conclusion_names(news_words)

            rule_category = dict()
            suggested_categories = []
            rule_output = str(test_n.id) + '\n'
            # Testing purpose, estimate rule support
            for result in results:
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
                                    result.rule.get_support() >= min_support or (
                                        result.rule.get_confidence() >= min_confidence_with_support and
                                        result.rule.get_support() >= min_support_with_confidence)):
                    suggested_categories.append(category)
                    rule_category[category] = result.rule.__str__()
                    # labels.update({category: category})

            if results:
                # Get at least best confidence and support categories
                min_rule_confidence = results[0].rule.get_confidence()
                for result in results:
                    category = result.category
                    if result.rule.get_confidence() == min_rule_confidence and category not in suggested_categories:
                        suggested_categories.append(category)
                        rule_category[category] = result.rule.__str__()
                    else:
                        break
                results.sort(key=lambda x: x.rule.get_support(), reverse=True)
                min_rule_support = results[0].rule.get_support()
                for result in results:
                    category = result.category
                    if result.rule.get_support() == min_rule_support and category not in suggested_categories:
                        suggested_categories.append(category)
                        rule_category[category] = result.rule.__str__()
                    else:
                        break

            for category in suggested_categories:
                rule_text = rule_category[category]
                news_suggested_category = PueblosNoticiasTestCategorias(
                    id=None, noticia_test=test_n, categorias_sugeridas=category, regla=rule_text)
                news_suggested_category.save()

            n = PueblosNoticias.objects.get(id=test_n.noticia_id)
            categories = n.get_categorias_string()
            clean_categories = []
            for category in categories:
                category = 'ETIQUETA_' + re.sub(ur'[ ]', '_', category.lower())
                category = clean_accents(category)
                clean_categories.append(category)
                # labels[category] = category
                # labels.update({category: category})
            news_results[test_n.noticia_id] = [clean_categories, suggested_categories]
        # cm_labels = labels.keys()
        # cm = ConfusionMatrix(labels=cm_labels)
        total_elements = 0.0
        correct_result = 0.0
        for n, list_categories in news_results.items():
            stored_categories, suggested_categories = list_categories
            n_stored += len(stored_categories)
            n_suggested += len(suggested_categories)
            if sm.check_correct(stored_categories, suggested_categories):
                result_text = ' Si contiene las etiquetas'
                correct_result += 1.0
            else:
                result_text = ' No contiene las etiquetas'
            total_elements += 1.0
            output += 'id ' + str(n) + ';stored ' + str(stored_categories) + ';suggested' \
                      + str(suggested_categories) + result_text + '\n'
            # cm.set_values(previous_categories=stored_categories, suggested_categories=suggested_categories)
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
