#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from pueblos.SemanticMotor.ConfusionMatrix import ConfusionMatrix


class Command(BaseCommand):
    help = 'Prueba la matriz de confusion'

    def handle(self, *args, **options):
        labels = ["generales", "social", "juventud", "empleo", "cultura"]
        cm = ConfusionMatrix(labels)
        print cm

