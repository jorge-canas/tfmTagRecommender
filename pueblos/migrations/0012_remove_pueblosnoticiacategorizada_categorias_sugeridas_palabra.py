# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-18 17:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pueblos', '0011_auto_20161018_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pueblosnoticiacategorizada',
            name='categorias_sugeridas_palabra',
        ),
    ]
