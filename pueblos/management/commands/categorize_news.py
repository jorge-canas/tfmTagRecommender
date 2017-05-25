#!/usr/bin/env python
# -*- coding: utf-8 -*-
from StringIO import StringIO

from django.core.management import call_command
from django.db import connection
from django.core.management.base import BaseCommand
from pueblos.common.util.utilities import get_news_without_category


class Command(BaseCommand):
    """Use example:
        python manage.py categorize_news 50
    """
    help = 'Coge noticias sin categorias'

    def add_arguments(self, parser):
        parser.add_argument('number_of_news', nargs='?', type=int, default=0, help='Numero de noticias a coger')
        parser.add_argument('--categorized', action='store_true', dest='categorized', default=False,
                            help='Coger noticias categorizadas')

    def handle(self, *args, **options):
        if options['number_of_news']:
            categorized = options['categorized']
            with connection.cursor() as cursor:
                limit = options['number_of_news']
                for x in range(0, limit):
                    news_id = get_news_without_category(categorized)
                    if news_id:
                        errbuf = StringIO()
                        buf = StringIO()
                        call_command('suggest_category_news', news_id=news_id, stdout=buf, stderr=errbuf)
                        print buf.getvalue()
                        print errbuf.getvalue()
                    else:
                        return self.stdout.write('No quedan noticias sin categorizar')

                return self.stdout.write('Finished')
        else:
            self.stderr.write('Number of news not set, please provide this parameters')
