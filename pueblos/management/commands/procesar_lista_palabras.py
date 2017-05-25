#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from pueblos.models import PueblosNoticias200, PueblosNoticiasPalabras, PueblosPalabrasEliminar, \
    PueblosDiccionarioSintactico

from pueblos.common.util.utilities import clean_text, esta, clean_accents
from django.db.utils import IntegrityError

import re


# Para lanzarlo
# ./manage.py procesar_lista_palabras [--use_syn_dict]


class Command(BaseCommand):
    help = 'Genera la lista de palabras asociado a cada noticia'

    def add_arguments(self, parser):
        parser.add_argument(
            '--use_syn_dict', action='store_true', dest='use_syn_dict', default=False,
            help='Usar el diccionario sintactico para sustituir algunas palabras incorrectas')

    def handle(self, *args, **options):
        use_syn_dict = options['use_syn_dict']
        news = PueblosNoticias200.objects.all()
        delete_words = PueblosPalabrasEliminar.objects.all()
        syntactic_dictionary = PueblosDiccionarioSintactico.objects.all()
        syn_dict = {}
        new_words = {}
        if use_syn_dict:
            self.stdout.write('Procesar lista de palabras - Using syn dict')
            for sd in syntactic_dictionary:
                syn_dict[sd.word] = sd.replace_word
        dont_save = []
        for word in delete_words:
            dont_save.append(word.palabra)
        # print dont_save
        # maximum = len(news)
        # self.stdout.write("hay " + str(maximum) + " por visitar")
        count = 1
        for n in news:
            # self.stdout.write(str(count) + " de " + str(maximum))
            count += 1
            # word_news = PueblosNoticiasPalabras.objects.filter(noticia_200=n.id)
            # if word_news.count() == 0:
            # limpiar signos de puntuacion y mas de 1 espacio
            words_list = re.sub(ur'[^a-zA-ZÁÉÍÓÚÜáéíóúüñÑ]', ' ', n.dscuerpo)

            # Transformar acentos en su letra
            words_list = words_list.lower()
            words_list = clean_accents(words_list)
            words_list = re.sub(ur'[ ]+', ' ', words_list)

            # separar las palabras en una lista para poder limpiar el texto
            words_list = words_list.split(' ')
            words_list[:] = [x.strip().lower() for x in words_list if not clean_text(x) and x not in dont_save]
            words_list.sort()

            """
                Replace the words of the news with the syntactic dictionary words
            """

            for index, word in enumerate(words_list):
                if word in syn_dict:
                    if use_syn_dict:
                        if len(syn_dict[word]) >= 3:  # The word is changed
                            # print words_list[index] + ' se cambia por ' + syn_dict[word]
                            words_list[index] = syn_dict[word]
                else:
                    # The word is stored in the dictionary so it can be saved later
                    new_words[word] = None

            # Generar diccionario de palabras, teniendo en cuenta la distancia levenshtein
            hashmap = {}
            plural = {}
            w = words_list.pop(0)
            hashmap[w] = w
            for w in words_list:
                if w[-1:] == 's' and len(w) > 4:  # word ends in 's' and is larger than 4 (3 without the s)
                    plural[w] = w
                else:
                    if not esta(w, hashmap):
                        hashmap[w] = w

            # Si es posible añadir singularizacion
            for key, w in plural.items():  # se busca si existen palabras parecidas en singular, sino se almacena
                # print '-------------------------------------Plurales--------------------'
                found = False
                check_ces = False
                word = w
                if w[-3:] == 'ces' and len(w) > 5:
                    w = w[:-3] + 'z'
                    check_ces = True
                if w[-2:] == 'es' and len(w) > 5:
                    w = w[:-1]  # se quita la s final
                    if not esta(w[:-1], hashmap):
                        found = True
                        hashmap[word] = word
                if not found and not esta(w, hashmap):
                    hashmap[word] = word
                if not check_ces and not esta(word[:-1], hashmap):  # Caso en el que ces se cambia por ce en lugar de z
                    hashmap[word] = word
            # print '----------------------'
            for key, word in hashmap.items():
                # print word
                n_word = PueblosNoticiasPalabras(id=None, noticia_200=n, palabra=word)
                try:
                    n_word.save()
                except IntegrityError as e:
                    if not e[0] == 1062:
                        raise
                    else:
                        message = 'Error: Entrada duplicada en palabras noticias. Esta accion se pudo haber' \
                                  ' completado previamente'
                        return self.stderr.write(message)
        for word, replace_word in new_words.items():
            new_word = PueblosDiccionarioSintactico(id=None, word=word)
            try:
                new_word.save()
            except IntegrityError as e:
                if not e[0] == 1062:
                    raise
                else:
                    message = 'Error: Entrada duplicada en diccionario sintactico. Esta accion se pudo haber ' \
                              'completado previamente'
                    # return self.stderr.write(message)

        return self.stdout.write('Finished')
