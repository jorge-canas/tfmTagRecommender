#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from pueblos.models import PueblosNoticiasPalabras
from collections import defaultdict


class Command(BaseCommand):
    help = 'Ver las palabras por categoria'

    def handle(self, *args, **options):
        palabras_categoria = defaultdict(dict)
        # palabras = PueblosNoticiasPalabras.objects.all()[:1000]
        palabras = PueblosNoticiasPalabras.objects.filter(palabra='ayuntamiento')
        for palabra in palabras:
            categorias = palabra.get_categorias_string()
            my_word = palabra.palabra
            # print 'La palabra a comprobar es ' + palabra.palabra
            for categoria in categorias:
                if my_word in palabras_categoria and categoria in palabras_categoria[my_word]:
                    palabras_categoria[my_word][categoria] += 1
                else:
                    palabras_categoria[my_word][categoria] = 1
        print 'Terminado diccionario'
        for word, category in palabras_categoria.items():
            for cat, value in category.items():
                print 'Para la palabra ' + word + ' y la categoria '+ cat + ' hay ' + str(value) + ' repeticiones'