# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-31 15:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pueblos', '0022_auto_20170126_1329'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pueblostestcase',
            old_name='n_notices',
            new_name='n_news',
        ),
        migrations.RenameField(
            model_name='pueblostestcase',
            old_name='n_notices_test',
            new_name='n_news_test',
        ),
    ]
