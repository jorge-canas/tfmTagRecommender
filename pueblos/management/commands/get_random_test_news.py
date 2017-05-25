# -*- coding: utf-8 -*-

import re

from django.core.management.base import BaseCommand
from pueblos.common.util.utilities import clean_accents
from pueblos.models import PueblosNoticiasTest, PueblosNoticiasTestCategorias


class Command(BaseCommand):
    """Use example:
     python manage.py test_context_set_matrix --test_file prueba_words_category.csv --output_file confusion_matrix"""
    help = 'Realiza el test del contexto creado y genera matrix de confusion'

    def add_arguments(self, parser):
        parser.add_argument('--number_of_news', dest='number_of_news', nargs='?', default='3',
                            help='Numero de noticias de test a coger')
        parser.add_argument('--output_file', dest='output_file', nargs='?', default='',
                            help='Nombre del fichero donde se guardara la matriz de confusion')

    def handle(self, *args, **options):
        output_file = options['output_file']
        savefile = 'files/random_categorized_news.txt'
        if output_file:
            if 'files_batch/' in output_file:
                savefile = output_file
            elif 'files/' not in output_file:
                savefile = 'files/' + output_file

            if '.txt' not in savefile:
                savefile = output_file + '.txt'
        with open(savefile, 'w') as f:
            number_of_news = options['number_of_news']
            text = ""

            news = PueblosNoticiasTest.objects.order_by('?')[:number_of_news]
            for n in news:
                text += 'Id noticia ' + str(n.noticia.id) + ' Id noticia test ' + str(n.id) + '\n'
                text += n.dscuerpo + '\n\n'
                text += 'Categorias guardadas\n'
                categories = n.get_categorias_string()
                for category in categories:
                    category = 'ETIQUETA_' + re.sub(ur'[ ]', '_', category.lower())
                    category = clean_accents(category)
                    text += category + ', '
                text += '\nCategorias sugeridas\n'
                suggested_categories = PueblosNoticiasTestCategorias.objects.filter(noticia_test=n)
                if len(suggested_categories) == 0:
                    text += '[]'
                else:
                    for suggested_category in suggested_categories:
                        text += suggested_category.categorias_sugeridas + ', '
                text += '\n\n\n'
            text = text.encode('utf-8')
            f.write(text)
            return self.stdout.write('Finished')
