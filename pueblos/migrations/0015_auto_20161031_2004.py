# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-31 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pueblos', '0014_auto_20161031_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pueblosdiccionariosintactico',
            name='replace_word',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]