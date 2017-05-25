#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from pueblos.models import PueblosPalabrasEliminar, PueblosDiccionarioSintactico


class Command(BaseCommand):
    help = 'Carga y genera base de datos de palabras a eliminar'

    def handle(self, *args, **options):
        filename = './pueblos/docs/lista_palabras_eliminar.txt'
        with open(filename) as fp:
            for line in fp:
                line = line.strip()
                if len(line) >= 3:
                    word = PueblosPalabrasEliminar.objects.filter(palabra=line)
                    if not word.exists():
                        delete_word = PueblosPalabrasEliminar(palabra=line)
                        delete_word.save()
        return self.stdout.write('Finished')
