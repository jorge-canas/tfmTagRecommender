#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from django.core.management.base import BaseCommand
from pueblos.SemanticMotor.ConfusionMatrix import ConfusionMatrix
from pueblos.common.util.utilities import clean_accents
from pueblos.SemanticMotor.SemanticMotor import SemanticMotor
from pueblos.models import PueblosNoticias


class Command(BaseCommand):
    """Use example:
     python manage.py test_context_set_matrix --test_file prueba_words_category.csv --output_file confusion_matrix"""
    help = 'Realiza el test del contexto creado y genera matrix de confusion'

    def add_arguments(self, parser):
        parser.add_argument('--test_file', dest='test_file', nargs='?', default='',
                            help='Nombre del fichero del conjunto de test')
        parser.add_argument('--output_file', dest='output_file', nargs='?', default='',
                            help='Nombre del fichero donde se guardara la matriz de confusion')

    def handle(self, *args, **options):
        n_stored = 0
        n_suggested = 0
        output = ''
        output_file = options['output_file']
        test_file = options['test_file']
        savefile = 'files/confusion_matrix.csv'
        if test_file:
            if '.csv' not in test_file:
                filename = test_file + '.csv'
            else:
                filename = test_file
        else:
            return self.stdout.write('Es necesario proporcionar un fichero de test')
        if output_file:
            if 'files_batch/' in output_file:
                savefile = output_file
            elif 'files/' not in output_file:
                savefile = 'files/' + output_file

            if '.csv' not in savefile:
                savefile = output_file + '.csv'

        sm = SemanticMotor()
        # sm.save_semantic_motor('files/semantic_motor.txt')
        with open(filename) as f:
            notice_results = {}
            labels = {}
            for line in f:
                parts = line.split(';')
                notice_id = parts.pop(0)
                results = sm.get_conclusion_names(parts)
                suggested_categories = []
                for result in results:
                    category = result.category
                    if category not in suggested_categories:
                        suggested_categories.append(category)
                    labels[category] = category

                notice = PueblosNoticias.objects.get(id=notice_id)
                categories = notice.get_categorias_string()
                clean_categories = []
                for category in categories:
                    category = 'ETIQUETA_' + re.sub(ur'[ ]', '_', category.lower())
                    category = clean_accents(category)
                    clean_categories.append(category)
                    labels[category] = category
                notice_results[notice_id] = [clean_categories, suggested_categories]
            labels = labels.keys()
            cm = ConfusionMatrix(labels=labels)
            for notice, list_categories in notice_results.items():
                stored_categories, suggested_categories = list_categories
                n_stored += len(stored_categories)
                n_suggested += len(suggested_categories)
                output += 'id ' + str(notice) + ';stored ' + str(stored_categories) + ';suggested' \
                          + str(suggested_categories) + '\n'
                cm.set_values(previous_categories=stored_categories, suggested_categories=suggested_categories)

            output += 'Total number of stored categories ' + str(n_stored) + '\n'
            output += 'Total number of suggested categories ' + str(n_suggested) + '\n'
            # print cm
            message = cm.save_confusion_matrix(savefile)
            if message is 'Saved':
                # Quit the .csv extension
                results_file = savefile[:-4]
                with open(results_file + '-track.txt', 'w') as fout:
                    fout.write(output.encode('utf-8'))
                with open(results_file + '-results.txt', 'w') as fout:
                    fout.write(cm.get_results())
                self.stdout.write('Finished')
            else:
                self.stdout.write('Error opening the output file')
