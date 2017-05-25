#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from pueblos.models import PueblosNoticias200, PueblosNc, PueblosCategoriasSemandal
from pueblos.models import PueblosNoticiasPalabras

from pueblos.common.util.utilities import clean_text, levenshtein

from collections import OrderedDict, defaultdict
from operator import itemgetter
import string
import re

class Command(BaseCommand):
    help = 'Ve la categoria de una noticia'

    def handle(self, *args, **options):
        palabras = PueblosNoticiasPalabras.objects.get(id=1116)
        categorias = palabras.get_categorias_id()
        print 'La palabra a comprobar es ' + palabras.palabra
        lista_indices = {}
        for categoria in categorias:
            categoria_string = PueblosCategoriasSemandal.objects.get(id=categoria)
            indice = palabras.get_indice(categoria)
            # print 'Indice para la palabra '+ palabras.palabra + ' en la categoria ' + categoria_string.dscategoria
            # print indice
            lista_indices[categoria_string.dscategoria] = indice

        for cat, value in lista_indices.items():
            print cat + ' tiene un indice ' + str(value)

        """
        palabras = PueblosNoticiasPalabras.objects.all()
        contador = 1
        print len(palabras)
        for palabra in palabras:
            print str(contador) + ' ' +palabra.palabra
            contador += 1
            categorias = palabra.get_categorias_string()
            for categoria in categorias:
                print '------------' + categoria
        """

        """
        noticia = PueblosNoticias200.objects.first()
        pueblosNc = PueblosNc.objects.filter(noticia=noticia.noticia)
        for pueblonc in pueblosNc:
            print pueblonc
            categoria = PueblosCategoriasSemandal.objects.get(id=pueblonc.categoria)
            print categoria.dscategoria
        """