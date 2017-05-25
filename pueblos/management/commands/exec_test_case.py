#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management import call_command
from django.core.management.base import BaseCommand
from StringIO import StringIO
from pueblos.models import PueblosTestCase


class Command(BaseCommand):
    help = 'Gestiona los test de la base de datos'

    def handle(self, *args, **options):
        test_cases = PueblosTestCase.objects.all()
        for test_case in test_cases:
            if test_case.state == 'not done':
                n_news = test_case.n_news
                n_news_test = test_case.n_news_test
                limit = test_case.limit
                confidence = test_case.confidence
                support = test_case.support
                use_syn_dict = test_case.use_syn_dict
                path_dir = 'test_cases/'
                output = 'test_case' + str(test_case.id)
                buf = StringIO()
                errbuf = StringIO()
                call_command('generate_test_case', n_news=n_news, n_news_test=n_news_test, limit=limit,
                             confidence=confidence, support=support, use_syn_dict=use_syn_dict, path=path_dir,
                             output=output, stdout=buf, stderr=errbuf)

                print 'return value'
                buf.seek(0)
                message = buf.read()
                print message
                if 'Problems' in message:
                    test_case.state = message
                else:
                    test_case.state = 'Finished'
                test_case.save()
