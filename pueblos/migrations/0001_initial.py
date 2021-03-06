# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-10 22:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PueblosCategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etiqueta', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'pueblos_categoria',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosCategoriasSemandal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dscategoria', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'pueblos_categorias_semandal',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosClassify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'pueblos_classify',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosComentarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dscomentario', models.CharField(max_length=200)),
                ('puntuacion', models.FloatField()),
                ('fecha', models.DateTimeField()),
            ],
            options={
                'db_table': 'pueblos_comentarios',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosDenunciasC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'pueblos_denuncias_c',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosLlamadas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('llamada', models.CharField(max_length=300)),
                ('contabilizacion', models.IntegerField()),
            ],
            options={
                'db_table': 'pueblos_llamadas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosLogUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_update', models.DateTimeField()),
            ],
            options={
                'db_table': 'pueblos_log_update',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosLogUpdateWeb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultado', models.IntegerField()),
            ],
            options={
                'db_table': 'pueblos_log_update_web',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosNc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'pueblos_nc',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosNoticias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dstitular', models.CharField(blank=True, max_length=1500, null=True)),
                ('dscuerpo', models.CharField(blank=True, max_length=50000, null=True)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('resumen', models.CharField(blank=True, max_length=2500, null=True)),
                ('url', models.CharField(blank=True, max_length=300, null=True)),
                ('liked', models.IntegerField()),
                ('fecha_ins', models.DateTimeField()),
            ],
            options={
                'db_table': 'pueblos_noticias',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosNvistas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'pueblos_nvistas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosProvincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dsprovincia', models.CharField(max_length=200, unique=True)),
                ('dspopcional', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('bprov', models.CharField(max_length=200, unique=True)),
                ('bprovop', models.CharField(blank=True, max_length=200, null=True, unique=True)),
            ],
            options={
                'db_table': 'pueblos_provincia',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosPueblo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dspueblo', models.CharField(max_length=200)),
                ('dsopcional', models.CharField(max_length=200)),
                ('cp', models.IntegerField()),
                ('latitud', models.DecimalField(blank=True, decimal_places=7, max_digits=11, null=True)),
                ('longitud', models.DecimalField(blank=True, decimal_places=7, max_digits=11, null=True)),
                ('busqueda', models.CharField(max_length=200)),
                ('busquedaop', models.CharField(max_length=200)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('opencms', models.IntegerField()),
                ('redirec', models.CharField(blank=True, max_length=200, null=True)),
                ('provincia_id', models.IntegerField()),
                ('habitantes', models.IntegerField(blank=True, null=True)),
                ('deuda', models.FloatField(blank=True, null=True)),
                ('deudaxhab', models.DecimalField(blank=True, decimal_places=7, max_digits=11, null=True)),
                ('densidad', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('superficie', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('fecha_ins', models.DateField()),
                ('wiki', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'pueblos_pueblo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosPuebloInfoextra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pueblo_id', models.IntegerField()),
                ('contrato_temp', models.IntegerField()),
                ('contrato_indef', models.IntegerField()),
                ('url_datos', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'pueblos_pueblo_infoextra',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosReglasOntologia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etiqueta_id', models.IntegerField()),
                ('subcategoria_de_id', models.IntegerField()),
            ],
            options={
                'db_table': 'pueblos_reglas_ontologia',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosSigp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user_id', models.IntegerField()),
                ('id_p_id', models.IntegerField()),
            ],
            options={
                'db_table': 'pueblos_sigp',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dsstatus', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'pueblos_status',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosTLiked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user_id', models.IntegerField()),
                ('id_n_id', models.IntegerField()),
            ],
            options={
                'db_table': 'pueblos_t_liked',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dsusuario', models.CharField(max_length=100, unique=True)),
                ('dsnombre', models.CharField(max_length=100)),
                ('dsapellido1', models.CharField(max_length=100)),
                ('dsapellido2', models.CharField(max_length=100)),
                ('pueblo_id', models.IntegerField()),
                ('token', models.CharField(max_length=200)),
                ('correo', models.CharField(blank=True, max_length=100, null=True, unique=True)),
            ],
            options={
                'db_table': 'pueblos_usuario',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosVecinos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id1_id', models.IntegerField()),
                ('id2_id', models.IntegerField()),
            ],
            options={
                'db_table': 'pueblos_vecinos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosVersions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tabla', models.CharField(max_length=20)),
                ('version', models.IntegerField()),
            ],
            options={
                'db_table': 'pueblos_versions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PueblosVotaciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_n_id', models.IntegerField()),
                ('id_user_id', models.IntegerField()),
                ('categoria_id', models.IntegerField()),
                ('votacion', models.IntegerField()),
            ],
            options={
                'db_table': 'pueblos_votaciones',
                'managed': False,
            },
        ),
    ]
