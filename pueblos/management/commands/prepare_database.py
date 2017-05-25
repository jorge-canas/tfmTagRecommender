#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management import call_command

from django.core.management.base import BaseCommand

from pueblos.models import PueblosNoticias200, PueblosNoticiasTest, PueblosNoticiasPalabras, PueblosRule, \
    PueblosConclusion, PueblosPremise


class Command(BaseCommand):
    """Use example:
     python manage.py clean_town_from_db"""
    help = 'Limpia base de datos y carga ficheros de datos'

    def add_arguments(self, parser):
        parser.add_argument('--dir_file', dest='dir_file', nargs='?', default='',
                            help='Localización de los ficheros de carga')

    def handle(self, *args, **options):
        dir_file = options['dir_file']
        news = 'testing/' + dir_file + '/dumpdatabase/news.json'
        news_test = 'testing/' + dir_file + '/dumpdatabase/news_test.json'
        PueblosNoticiasPalabras.objects.all().delete()
        PueblosNoticias200.objects.all().delete()
        PueblosNoticiasTest.objects.all().delete()
        PueblosPremise.objects.all().delete()
        PueblosConclusion.objects.all().delete()
        PueblosRule.objects.all().delete()
        call_command('loaddata', news, app_label='pueblos')
        call_command('loaddata', news_test, app_label='pueblos')
