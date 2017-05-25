#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from django.core.management.base import BaseCommand

from pueblos.common.util.utilities import get_list_words
from pueblos.models import PueblosDiccionarioSintactico, PueblosPalabrasEliminar, PueblosPueblo


class Command(BaseCommand):
    """Use example:
     python manage.py clean_town_from_db"""
    help = 'Elimina los nombres de los pueblos de la base de datos'

    def handle(self, *args, **options):
        towns = PueblosPueblo.objects.all()
        for town in towns:
            list_names = get_list_words(town.dspueblo)
            for name in list_names:
                if len(name) > 3:
                    word_list = PueblosDiccionarioSintactico.objects.filter(word__exact=name)
                    for word in word_list:
                        if len(word.replace_word) == 0:
                            if not PueblosPalabrasEliminar.objects.filter(palabra__exact=name).exists():
                                new_entry = PueblosPalabrasEliminar(palabra=name)
                                new_entry.save()
