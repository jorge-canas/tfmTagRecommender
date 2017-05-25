#!/usr/bin/python
# -*- coding: utf-8 -*-

from pueblos.models import PueblosNoticias200, PueblosNoticiasPalabras
from pueblos.common.util.utilities import clean_accents
from collections import defaultdict, OrderedDict
from django.core.management.base import BaseCommand
import re
import time
import math
import os


# Call example
# python manage.py generate_context 30 20


class Command(BaseCommand):
    help = 'Genera el contexto de las noticias, necesita dos argumentos enteros, un porcentaje y un límite máximo de ' \
           'words para el contexto'

    def add_arguments(self, parser):
        # parser.add_argument('percentage', type=int, nargs='?', default=0, help='porcentaje de words por categoria')
        parser.add_argument('limit', type=int, nargs='?', default=0, help='limite de words por categoria')
        parser.add_argument('--output', dest='output', type=str, nargs='?', default='',
                            help='Fichero de salida contexto')

    def handle(self, *args, **options):
        SITE_ROOT = os.path.abspath(os.path.dirname('__file__'))
        #  percentage = int(options['percentage'])
        limit = int(options['limit'])

        news = PueblosNoticias200.objects.all()

        if not options['output']:
            filename = SITE_ROOT + '/files/' + 'context' + '-' + str(time.strftime('%d%m%Y')) + '-' + \
                       str(len(news)) + '-' + str(limit) + '.csv'
        else:
            filename = options['output'] + '-' + str(len(news)) + '-' + str(limit) + '.csv'
        """
        if limit >= 30:
            limit = 30
        """
        writer = open(filename, 'w')
        output_file = filename[:-4] + '-context-track.csv'

        # Crea diccionario con categorías y sus words asociadas
        categories_word = defaultdict(dict)
        word_categories = defaultdict(dict)
        total_words_category = {}
        words = PueblosNoticiasPalabras.objects.all()  # todos

        for word in words:
            my_word = word.palabra
            if 3 < len(my_word) < 30:
                categories = word.get_categorias_string()
                for category in categories:
                    label = 'ETIQUETA_' + re.sub(ur'[ ]', '_', category.lower())
                    label = clean_accents(label)

                    if label not in categories_word:
                        categories_word[label][my_word] = 1.0
                    elif my_word not in categories_word[label]:
                        categories_word[label][my_word] = 1.0
                    else:
                        categories_word[label][my_word] += 1.0

                    # Number of different words for each category
                    if my_word not in word_categories:
                        word_categories[my_word][label] = 1.0
                    elif label not in word_categories[my_word]:
                        word_categories[my_word][label] = 1.0

                    if label not in total_words_category:
                        total_words_category[label] = 1.0
                    else:
                        total_words_category[label] += 1.0

        # print total_words_category
        # self.stdout.write('Terminado diccionario')

        # Genera los índices para cada word según la fórmula: TF*IDF
        total_words_category = OrderedDict(
            sorted(total_words_category.items(), key=lambda x: x[1], reverse=True))
        max_category = {}
        # print total_words_category
        total_cat = float(len(total_words_category))

        for category, words in categories_word.items():
            # print category
            categories_word[category] = OrderedDict(sorted(words.items(), key=lambda x: x[1], reverse=True))
            # valor del primer elemento de la lista es la mayor repeticion para esa categoria
            max_category[category] = categories_word[category].items()[0][1]

            # print '------------------'
            # print categories_word[category[0]]
        # print max_category
        # print max_category[u'ETIQUETA_regimen_interior']
        output = ''
        with open(output_file, 'w') as f:
            f.write(output)
        counter = 0
        for category, words in categories_word.items():
            # print words
            for word, value in words.items():
                TF = value / max_category[category]
                IDF = total_cat / float(len(word_categories[word].items()))
                # print str(len(word_categories[word].items()))
                # print word_categories[word].items()
                IDF = math.log(IDF, 10)
                TF_IDF = TF * IDF
                categories_word[category][word] = TF_IDF
                output += category + ';' + word + '; TF ' + str(TF) + ' (value/max_category  ' + str(
                    value) + '/' + str(max_category[category]) + ') IDF ' + str(
                    IDF) + ' (log10(n_category/n_category_aparece_word)) ' + str(total_cat) + '/' + str(
                    float(len(word_categories[word].items()))) + ') TF*IDF; ' + str(TF_IDF) + '\n'
                counter += 1
                # To avoid run out of memory, the output is append to the file and reset
                if counter % 100 == 0:
                    with open(output_file, 'a') as f:
                        output = output.encode('utf-8')
                        f.write(output)
                        output = ''
                # print categories_word[category][word]
        if output:
            with open(output_file, 'a') as f:
                output = output.encode('utf-8')
                f.write(output)

        for category, words in categories_word.items():
            categories_word[category] = OrderedDict(sorted(words.items(), key=lambda x: x[1], reverse=True))

        # TODO revisar maximo
        # Max words por categoría a guardar
        #  max_percentage = percentage / 100.0
        max_words = limit
        max_words_category = {}

        for category, value in total_words_category.items():
            if value <= max_words:
                max_words_category[category] = value
            else:
                """
                this_max = value * max_percentage

                if this_max > max_words:
                    this_max = max_words
                max_words_category[category] = this_max
                """
            max_words_category[category] = limit
        # print max_words_category[u'ETIQUETA_regimen_interior']
        # categories_words_limit = defaultdict(dict)
        # print max_words_category
        categories_words_limit = []
        for category, words in categories_word.items():
            limit = 0
            for w, value in words.items():
                if limit < max_words_category[category]:
                    limit += 1
                    if w not in categories_words_limit:
                        categories_words_limit.append(w)
                else:
                    break

        # self.stdout.write('Terminados indices')

        # Preparar elementos para generar archivo
        list_cat_pal = []
        for category, word in categories_word.items():
            list_cat_pal.append(category)

        for word in categories_words_limit:
            list_cat_pal.append(word)

        list_cat_pal.sort()
        # print list_cat_pal
        # cabecera

        # Formato
        """
        primera línea: Lista de atributos, en este caso categorías y words
        resto de líneas - objetos: Primer elemento id de la noticia, resto words con buen índice en la noticia
        """
        line = ''
        for w in list_cat_pal:
            line += w + ';'
        line = line.encode('utf-8')
        # print line
        writer.write(line[:-1] + '\n')

        for n in news:
            line = str(n.id) + ';'
            # Categorias asociadas a la noticia
            categories = n.get_categorias_string()
            for category in categories:
                label = 'ETIQUETA_' + re.sub(ur'[ ]', '_', category.lower())
                label = clean_accents(label)
                line += label + ';'

            word_news = PueblosNoticiasPalabras.objects.filter(noticia_200=n.id)
            list = []
            for w in word_news:
                list.append(w.palabra)
                list.sort()
            # print list

            for word in list:
                if word in list_cat_pal:
                    line += word + ';'
            line = line.encode('utf-8')
            writer.write(line[:-1] + '\n')
        writer.close()
        return self.stdout.write('Finished')
