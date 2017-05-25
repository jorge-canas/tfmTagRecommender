#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from subprocess import Popen, STDOUT
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Use example:
         python manage.py generate_store_rules --ctx files/context.csv --output files/num_rules_info.txt"""
    help = 'Genera la base de reglas del contexto pasado como argumento'

    def add_arguments(self, parser):
        parser.add_argument('--ctx', dest='ctx', type=str, nargs='?', default='', help='Fichero de contexto')
        parser.add_argument('--output', dest='output', type=str, nargs='?', default='', help='Fichero de salida')

    def handle(self, *args, **options):
        if options['ctx'] and options['output']:
            # self.stdout.write(options['ctx'])
            # self.stdout.write(options['output'])
            """
            cmd = ["java", "-jar", "jar/context-generator.jar", "GenerateRulesAndStore", "-ctx",
                   options['ctx']]
            """
            """
            cmd = ["java", "-jar", "jar/context-generator.jar", "GenerateRulesAndStore", "-Xms2048m", "-Xmx6144m",
                   "--ctx", options['ctx']]
            filename = options['output']
            with open(filename, mode="w") as f:
                Popen(cmd, stdout=f, stderr=STDOUT)
            """
            command = "java -jar jar/context-generator.jar GenerateRulesAndStore -Xms2048m -Xmx6144m --ctx " + \
                      options['ctx'] + " > " + options['output']
            self.stdout.write(command)
            os.system(command)
            self.stdout.write('Finished')
        elif not options['ctx'] and not options['output']:
            self.stderr.write('Context and output files not set, provide one after --ctx and --output')
        elif not options['ctx']:
            self.stderr.write('Context file not set, provide one after --ctx')
        elif not options['output']:
            self.stderr.write('Output file not set, provide one after --output')
