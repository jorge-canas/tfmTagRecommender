# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-11 16:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pueblos', '0019_auto_20170111_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pueblostestcase',
            name='conf_support',
        ),
        migrations.RemoveField(
            model_name='pueblostestcase',
            name='sup_confidence',
        ),
    ]
