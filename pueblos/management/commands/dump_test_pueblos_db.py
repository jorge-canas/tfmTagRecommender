#!/usr/bin/python
# -*- coding: utf-8 -*-
from StringIO import StringIO
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Use example:
     python manage.py test_context_set_matrix --test_file prueba_words_category.csv --output_file confusion_matrix"""
    help = 'Realiza el test del contexto creado y genera matrix de confusion'

    def add_arguments(self, parser):
        parser.add_argument('--output_dir', dest='output_dir', nargs='?', default='confusion_matrix',
                            help='Nombre del fichero donde se guardara la matriz de confusion')

    def handle(self, *args, **options):
        if not options['output_dir']:
            output_dir = 'dumpdatabase/'
        else:
            if not options['output_dir'][-1:] == '/':
                output_dir = options['output_dir'] + '/'
            else:
                output_dir = options['output_dir']

        rules = output_dir + 'rule.json'
        conclusion = output_dir + 'conclusion.json'
        premise = output_dir + 'premise.json'
        news = output_dir + 'news.json'
        news_test = output_dir + 'news_test.json'
        news_test_categories = output_dir + 'news_test_categories.json'

        with open(rules, 'w') as f:
            call_command('dumpdata', 'pueblos.PueblosRule', indent=2, stdout=f)
        with open(conclusion, 'w') as f:
            call_command('dumpdata', 'pueblos.PueblosConclusion', indent=2, stdout=f)
        with open(premise, 'w') as f:
            call_command('dumpdata', 'pueblos.PueblosPremise', indent=2, stdout=f)
        with open(news, 'w') as f:
            call_command('dumpdata', 'pueblos.PueblosNoticias200', indent=2, stdout=f)
        with open(news_test, 'w') as f:
            call_command('dumpdata', 'pueblos.PueblosNoticiasTest', indent=2, stdout=f)
        with open(news_test_categories, 'w') as f:
            call_command('dumpdata', 'pueblos.PueblosNoticiasTestCategorias', indent=2, stdout=f)

        self.stdout.write('Finished')
