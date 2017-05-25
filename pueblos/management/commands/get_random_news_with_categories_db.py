#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import connection
from django.core.management.base import BaseCommand
from pueblos.models import PueblosNoticiasTest, PueblosNoticiasTestCategorias


class Command(BaseCommand):
    """Use example:
        python manage.py get_random_news_with_categories 50
    """
    help = 'Genera la lista de noticias de test'

    def add_arguments(self, parser):
        parser.add_argument('number_of_news', nargs='?', type=int, default=0, help='Numero de noticias a coger')

    def handle(self, *args, **options):
        if options['number_of_news']:
            """
            Clean previous news with categories
            """
            PueblosNoticiasTest.objects.all().delete()
            PueblosNoticiasTestCategorias.objects.all().delete()
            with connection.cursor() as cursor:
                limit = options['number_of_news']
                query = """
                    INSERT INTO pueblos_noticias_test(noticia_id, dscuerpo, dstitular)
                    SELECT DISTINCT noticia.id, noticia.dscuerpo, noticia.dstitular
                    FROM pueblos_noticias noticia
                    LEFT JOIN pueblos_noticias_200 noticia200
                        ON noticia200.noticia_id = noticia.id
                    INNER JOIN pueblos_nc nc
                        ON noticia.id = nc.noticia_id
                            AND nc.categoria_id != 53
                            AND length(noticia.dscuerpo) > 200
                    WHERE noticia200.noticia_id IS NULL
                    AND noticia.dscuerpo REGEXP '^[A-Za-z0-9ÁÉÍÓÚÜáéíóúüñÑ \t\n?=_+-.,!@#\€\¡\¿$%%^&*()\º\ª;:\\\/|<>"''-~[]+$'
                    ORDER BY RAND()
                    LIMIT %s
                    """
                cursor.execute(query, (int(limit),))
                # return self.stdout.write('Finished with ' + str(count) + ' news returned')
                return self.stdout.write('Finished')
        else:
            self.stderr.write('Number of news not set, please provide this parameters')
