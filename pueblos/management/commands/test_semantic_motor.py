#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from pueblos.SemanticMotor.SemanticMotor import SemanticMotor, Rule


class Command(BaseCommand):
    help = 'Prueba el motor semantico'

    def handle(self, *args, **options):
        sm = SemanticMotor()
        rules = [Rule(20, 1, ['ayuntamiento'], ['ETIQUETA_general']),
                 Rule(10, 1, ['centro', 'plaza'], ['ETIQUETA_educacion', 'docente', 'ETIQUETA_cursos']),
                 Rule(4, 0.8, ['acta', 'gestion', 'tecnico'], ['calificacion', 'ETIQUETA_empleo'])]
        sm.rules = rules
        print 'Test 1'
        facts = ['juventud', 'ayuntamiento', 'centro', 'plaza', 'docente']

        results = sm.get_conclusion_names(facts)
        for result in results:
            # print result.__str__()
            print result.category
        print 'Expected: general, educacion, cursos'

        print 'Test 2'
        facts = ['acta', 'plaza', 'gestion', 'tecnico', 'calificacion']

        results = sm.get_conclusion_names(facts)
        for result in results:
            # print result.__str__()
            print result.category
        print 'Expected: empleo'

        print 'Test 3'
        facts = ['plaza', 'gestion', 'banco', 'libre']

        results = sm.get_conclusion_names(facts)
        for result in results:
            # print result.__str__()
            print result.category
        print 'Expected: -'
