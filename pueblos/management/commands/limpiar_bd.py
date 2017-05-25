#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import connection
from django.core.management.base import BaseCommand
from pueblos.models import PueblosNoticias200, PueblosNoticiasPalabras

"""
Call example
python manage.py limpiar_bd --delete 400 # delete all news and words and select 400 random categorized news
python manage.py limpiar_bd # delete all words from PueblosNoticiasPalabras
"""


class Command(BaseCommand):
    help = 'Elimina las palabras de las noticias e incluso genera una nueva lista de noticias'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--delete', action='store_true', dest='delete', default=False, help='Elimina y genera las noticias')
        parser.add_argument('number_of_news', type=int, nargs='?', default=0, help='Numero de noticias a coger')

    def handle(self, *args, **options):
        PueblosNoticiasPalabras.objects.all().delete()
        if options['delete']:
            PueblosNoticias200.objects.all().delete()

            cursor = connection.cursor()
            limit = options['number_of_news']
            query = """
                INSERT INTO pueblos_noticias_200(dstitular, dscuerpo, noticia_id)
                SELECT DISTINCT noticia.dstitular, noticia.dscuerpo, noticia.id
                FROM pueblos_noticias AS noticia
                INNER JOIN pueblos_nc AS nc
                ON noticia.id = nc.noticia_id 
                    AND nc.categoria_id != 53 
                    AND length(noticia.dscuerpo) > 400
                WHERE noticia.dscuerpo REGEXP '^[A-Za-z0-9ÁÉÍÓÚÜáéíóúüñÑ \t\n?=_+-.,!@#\€\¡\¿$%%^&*()\º\ª;:\\\/|<>"''-~[]+$'
                ORDER BY RAND() 
                LIMIT %s
                """
            try:
                cursor.execute(query, (int(limit),))
            finally:
                cursor.close()

            self.stdout.write(self.style.SUCCESS('Seleccionadas %s noticias' % limit))
            return self.stdout.write(self.style.SUCCESS('Finished'))
        else:
            return self.stdout.write(self.style.SUCCESS('Finished'))
