#!/usr/bin/python
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, STDOUT
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Prueba del jar'

    def handle(self, *args, **options):
        cmd = ["java", "-jar", "jar/context-generator.jar", "GenerateRulesAndStore", "-ctx",
               "files/contexto10102016-50-5.csv"]
        filename = "files/numRulesInfo.txt"
        with open(filename, mode="w") as f:
            p = Popen(cmd, stdout=f, stderr=STDOUT)
        self.stdout.write('Finished')
