# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-07 11:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pueblos', '0015_auto_20161031_2004'),
    ]

    operations = [
        migrations.CreateModel(
            name='PueblosNoticiasTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dstitular', models.TextField(blank=True, max_length=1500, null=True)),
                ('dscuerpo', models.TextField(blank=True, max_length=50000, null=True)),
                ('noticia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pueblos.PueblosNoticias')),
            ],
            options={
                'db_table': 'pueblos_noticias_test',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PueblosNoticiasTestCategorias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorias_sugeridas', models.CharField(max_length=80)),
                ('noticia_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pueblos.PueblosNoticiasTest')),
            ],
            options={
                'db_table': 'pueblos_noticias_test_categorias',
                'managed': True,
            },
        ),
    ]