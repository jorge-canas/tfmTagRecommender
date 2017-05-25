#!/usr/bin/python
# -*- coding: utf-8 -*-

from pueblos.models import PueblosNoticias200, PueblosNoticiasPalabras
from pueblos.common.util.utilities import clean_accents
from collections import defaultdict, OrderedDict
from django.core.management.base import BaseCommand
from pueblos.common.util.utilities import save_file
import re
import time
import math
import os


# Call example
# python manage.py generate_context 30 20


class Command(BaseCommand):
    help = 'Genera el contexto de las noticias, necesita dos argumentos enteros, un porcentaje y un límite máximo de ' \
           'palabras para el contexto'

    def add_arguments(self, parser):
        parser.add_argument('percentage', type=int, nargs='?', default=0, help='porcentaje de palabras por categoria')
        parser.add_argument('limit', type=int, nargs='?', default=0, help='limite de palabras por categoria')
        parser.add_argument('--output', dest='output', type=str, nargs='?', default='',
                            help='Fichero de salida contexto')

    def handle(self, *args, **options):
        SITE_ROOT = os.path.abspath(os.path.dirname('__file__'))
        #  percentage = int(options['percentage'])
        limit = int(options['limit'])
        if limit > 21:
            limit = 20
        noticias = PueblosNoticias200.objects.all()

        if not options['output']:
            filename = SITE_ROOT + '/files/' + 'context' + '-' + str(time.strftime('%d%m%Y')) + '-' + \
                       str(len(noticias)) + '-' + str(limit) + '.csv'
        else:
            filename = options['output'] + '-' + str(len(noticias)) + '-' + str(limit) + '.csv'

        writer = open(filename, 'w')
        output_file = filename[:-4] + '-context-track.csv'
        output_file_order = filename[:-4] + '-ord-ctx-track.csv'
        output_file_order2 = filename[:-4] + '-ord2-ctx-track.csv'
        output_file_order3 = filename[:-4] + '-ord3-ctx-track.csv'

        # Crea diccionario con categorías y sus palabras asociadas
        categorias_palabra = defaultdict(dict)
        palabra_categorias = defaultdict(dict)
        total_palabras_categoria = {}
        palabras = PueblosNoticiasPalabras.objects.all()  # todos

        for palabra in palabras:
            my_word = palabra.palabra
            if 3 < len(my_word) < 30:
                categorias = palabra.get_categorias_string()
                for categoria in categorias:
                    etiqueta = 'ETIQUETA_' + re.sub(ur'[ ]', '_', categoria.lower())
                    etiqueta = clean_accents(etiqueta)

                    if etiqueta not in categorias_palabra:
                        categorias_palabra[etiqueta][my_word] = 1.0
                    elif my_word not in categorias_palabra[etiqueta]:
                        categorias_palabra[etiqueta][my_word] = 1.0
                    else:
                        categorias_palabra[etiqueta][my_word] += 1.0

                    # Number of different words for each category
                    if my_word not in palabra_categorias:
                        palabra_categorias[my_word][etiqueta] = 1.0
                    elif etiqueta not in palabra_categorias[my_word]:
                        palabra_categorias[my_word][etiqueta] = 1.0

                    if etiqueta not in total_palabras_categoria:
                        total_palabras_categoria[etiqueta] = 1.0
                    else:
                        total_palabras_categoria[etiqueta] += 1.0

        # print total_palabras_categoria
        # self.stdout.write('Terminado diccionario')

        # Genera los índices para cada palabra según la fórmula: TF*IDF
        total_palabras_categoria = OrderedDict(
            sorted(total_palabras_categoria.items(), key=lambda x: x[1], reverse=True))
        max_categoria = {}
        # print total_palabras_categoria
        total_cat = float(len(total_palabras_categoria))

        for category, words in categorias_palabra.items():
            # print category
            categorias_palabra[category] = OrderedDict(sorted(words.items(), key=lambda x: x[1], reverse=True))
            # valor del primer elemento de la lista es la mayor repeticion para esa categoria
            max_categoria[category] = categorias_palabra[category].items()[0][1]

            # print '------------------'
            # print categorias_palabra[category[0]]
        # print max_categoria
        # print max_categoria[u'ETIQUETA_regimen_interior']
        output = ''
        save_file(output_file, 'w', output)
        counter = 0
        for category, words in categorias_palabra.items():
            # print words
            for word, value in words.items():
                TF = value / max_categoria[category]
                IDF = total_cat / float(len(palabra_categorias[word].items()))
                # print str(len(palabra_categorias[word].items()))
                # print palabra_categorias[word].items()
                IDF = math.log(IDF, 10)
                TF_IDF = TF * IDF
                categorias_palabra[category][word] = TF_IDF
                output += category + ';' + word + '; TF ' + str(TF) + ' (value/max_categoria  ' + str(
                    value) + '/' + str(max_categoria[category]) + ') IDF ' + str(
                    IDF) + ' (log10(n_categorias/n_categorias_aparece_palabra)) ' + str(total_cat) + '/' + str(
                    float(len(palabra_categorias[word].items()))) + ') TF*IDF; ' + str(TF_IDF) + '\n'
                counter += 1
                # To avoid run out of memory, the output is append to the file and reset
                if counter % 100 == 0:
                    save_file(output_file, 'a', output)
                    output = ''
                # print categorias_palabra[category][word]
        if output:
            save_file(output_file, 'a', output)

        for category, words in categorias_palabra.items():
            categorias_palabra[category] = OrderedDict(sorted(words.items(), key=lambda x: x[1], reverse=True))

        index_limit = 1  # second element with best tf*idf
        min_tf_idf = float('inf')
        for category, words in categorias_palabra.items():
            # print words
            index = 0
            for word, value in words.items():
                if index == index_limit:
                    if value < min_tf_idf:
                        min_tf_idf = value
                        break
                index += 1

        # Ordered output
        header = str(min_tf_idf) + '\n'
        mean = 0.0
        n_categories = 0.0
        for category, words in categorias_palabra.items():
            header += category + ' ' + str(len(words)) + ';'
            mean += len(words)
            n_categories += 1.0
        mean /= n_categories
        header += '\nMean value ' + str(mean) + '\n'
        save_file(output_file_order, 'w', header)
        output = ''
        for category, words in categorias_palabra.items():
            # print words
            for word, TF_IDF in words.items():
                output += category + ';' + word + ';' + '{0:.2f}'.format(TF_IDF) + '\n'
                counter += 1
                # To avoid run out of memory, the output is append to the file and reset
                if counter % 100 == 0:
                    save_file(output_file_order, 'a', output)
                    output = ''
                # print categorias_palabra[category][word]
        if output:
            save_file(output_file_order, 'a', output)
        # End ordered output

        # Ordered output 2: limited to the same limit of the normal generate context (5, 10 or 20)
        limit_header = str(min_tf_idf) + '\n'
        mean = 0.0
        n_categories = 0.0
        for category, words in categorias_palabra.items():
            limit_words = 0.0
            for word, TF_IDF in words.items():
                if TF_IDF >= min_tf_idf:
                    limit_words += 1.0
                else:
                    break
            limit_header += category + ' ' + str(limit_words) + ';'
            mean += limit_words
            n_categories += 1.0
        mean /= n_categories
        limit_header += '\nMean value ' + str(mean) + '\n'
        output = ''
        save_file(output_file_order2, 'w', limit_header)
        for category, words in categorias_palabra.items():
            # print words
            index = 0
            for word, TF_IDF in words.items():
                if TF_IDF >= min_tf_idf and index < limit:
                    output += category + ';' + word + ';' + '{0:.2f}'.format(TF_IDF) + '\n'
                    counter += 1
                # To avoid run out of memory, the output is append to the file and reset
                if counter % 100 == 0:
                    save_file(output_file_order2, 'a', output)
                    output = ''
                        # print categorias_palabra[category][word]
                index += 1
        if output:
            save_file(output_file_order2, 'a', output)
        # End ordered output 2
        """
        # Ordered output 3: limited to 30 elements
        output = ''
        # max_elements = 5
        max_elements = 30
        save_file(output_file_order3, 'w', limit_header)
        for category, words in categorias_palabra.items():
            # print words
            index = 0
            for word, TF_IDF in words.items():
                if TF_IDF >= min_tf_idf and index < max_elements:
                    output += category + ';' + word + ';' + '{0:.2f}'.format(TF_IDF) + '\n'
                    counter += 1
                # To avoid run out of memory, the output is append to the file and reset
                if counter % 100 == 0:
                    save_file(output_file_order3, 'a', output)
                    output = ''
                        # print categorias_palabra[category][word]
                index += 1
        if output:
            save_file(output_file_order3, 'a', output)
        # End ordered output 3
        """
        limit_word_category = []
        for category, words in categorias_palabra.items():
            index = 0
            for w, value in words.items():
                if value >= min_tf_idf and index < limit:  # max_elements:
                    if w not in limit_word_category:
                        limit_word_category.append(w)
                else:
                    break
                index += 1

        # self.stdout.write('Terminados indices')

        # Preparar elementos para generar archivo
        list_cat_pal = []
        for category, word in categorias_palabra.items():
            list_cat_pal.append(category)

        for word in limit_word_category:
            list_cat_pal.append(word)

        list_cat_pal.sort()
        # print list_cat_pal
        # cabecera

        # Formato
        """
        primera línea: Lista de atributos, en este caso categorías y palabras
        resto de líneas - objetos: Primer elemento id de la noticia, resto palabras con buen índice en la noticia
        """
        line = ''
        for w in list_cat_pal:
            line += w + ';'
        line = line.encode('utf-8')
        # print line
        writer.write(line[:-1] + '\n')

        for noticia in noticias:
            line = str(noticia.id) + ';'
            # Categorias asociadas a la noticia
            categorias = noticia.get_categorias_string()
            for categoria in categorias:
                etiqueta = 'ETIQUETA_' + re.sub(ur'[ ]', '_', categoria.lower())
                etiqueta = clean_accents(etiqueta)
                line += etiqueta + ';'

            word_news = PueblosNoticiasPalabras.objects.filter(noticia_200=noticia.id)
            list = []
            for w in word_news:
                list.append(w.palabra)
                list.sort()
            # print lista

            for word in list:
                if word in list_cat_pal:
                    line += word + ';'
            line = line.encode('utf-8')
            writer.write(line[:-1] + '\n')
        writer.close()
        return self.stdout.write('Finished')
