#!/usr/bin/python
# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

"""
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class PueblosAmigode(models.Model):
    idamistad = models.ForeignKey('PueblosUsuario', models.DO_NOTHING)
    idamigode = models.ForeignKey('PueblosUsuario', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pueblos_amigode'
        unique_together = (('idamistad', 'idamigode'),)
"""


class PueblosPalabrasEliminar(models.Model):
    palabra = models.CharField(primary_key=True, max_length=60)

    class Meta:
        managed = True
        db_table = 'pueblos_palabras_eliminar'


class PueblosCategoriasSemandal(models.Model):
    dscategoria = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'pueblos_categorias_semandal'


class PueblosCategoria(models.Model):
    etiqueta_padre = models.ForeignKey('PueblosCategoriasSemandal', models.DO_NOTHING)
    etiqueta = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'pueblos_categoria'


class PueblosClassify(models.Model):
    id_n = models.ForeignKey('PueblosNoticias', models.DO_NOTHING)
    id_user = models.ForeignKey('PueblosUsuario', models.DO_NOTHING)
    c_new = models.ForeignKey('PueblosCategoriasSemandal', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pueblos_classify'
        unique_together = (('id_n', 'id_user', 'c_new'),)


class PueblosComentarios(models.Model):
    dscomentario = models.CharField(max_length=200)
    id_user = models.ForeignKey('PueblosUsuario', models.DO_NOTHING)
    id_not = models.ForeignKey('PueblosNoticias', models.DO_NOTHING)
    puntuacion = models.FloatField()
    fecha = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pueblos_comentarios'


class PueblosDenunciasC(models.Model):
    comentario = models.ForeignKey('PueblosComentarios', models.DO_NOTHING)
    id_user = models.ForeignKey('PueblosUsuario', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pueblos_denuncias_c'
        unique_together = (('id_user', 'comentario'),)


class PueblosLlamadas(models.Model):
    llamada = models.CharField(max_length=300)
    contabilizacion = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pueblos_llamadas'


class PueblosLogUpdate(models.Model):
    fecha_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pueblos_log_update'


class PueblosLogUpdateWeb(models.Model):
    update = models.ForeignKey('PueblosLogUpdate', models.DO_NOTHING)
    municipio = models.ForeignKey('PueblosPueblo', models.DO_NOTHING)
    resultado = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pueblos_log_update_web'
        unique_together = (('update', 'municipio'),)


class PueblosNc(models.Model):
    noticia = models.ForeignKey('PueblosNoticias', models.DO_NOTHING)
    categoria = models.ForeignKey('PueblosCategoriasSemandal', models.DO_NOTHING)
    confirmada = models.ForeignKey('PueblosStatus', models.DO_NOTHING)

    def __unicode__(self):
        value = 'noticia_id ' + str(self.noticia.id) + ' categoria_id ' + str(self.categoria.id)
        return value

    def __str__(self):
        return unicode(self).encode('utf-8')

    class Meta:
        managed = False
        db_table = 'pueblos_nc'
        unique_together = (('noticia', 'categoria'),)


class PueblosNoticias(models.Model):
    pueblo = models.ForeignKey('PueblosPueblo', models.DO_NOTHING)
    dstitular = models.CharField(max_length=1500, blank=True, null=True)
    dscuerpo = models.TextField(max_length=50000, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    resumen = models.CharField(max_length=2500, blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)
    liked = models.IntegerField()
    fecha_ins = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pueblos_noticias'

    def get_categorias_string(self):
        categorias = []
        noticia = PueblosNoticias.objects.get(id=self.id)
        pueblos_nc = PueblosNc.objects.filter(noticia=noticia)
        for pueblo_nc in pueblos_nc:
            categoria = PueblosCategoriasSemandal.objects.get(id=pueblo_nc.categoria.id)
            # print categoria.dscategoria
            categorias.append(categoria.dscategoria)
        return categorias

    def get_categorias_id(self):
        categorias = []
        noticia = PueblosNoticias.objects.get(id=self.id)
        pueblosNc = PueblosNc.objects.filter(noticia=noticia)
        for puebloNc in pueblosNc:
            categoria = PueblosCategoriasSemandal.objects.get(id=puebloNc.categoria.id)
            # print categoria.dscategoria
            categorias.append(categoria.id)
        return categorias

"""
    Tabla generada para pruebas y FCA
"""


class PueblosNoticias200(models.Model):
    # referencia noticia para poder ver sus categorias en PueblosNc
    noticia = models.ForeignKey('PueblosNoticias', on_delete=models.CASCADE)
    dstitular = models.TextField(max_length=1500, blank=True, null=True)
    dscuerpo = models.TextField(max_length=50000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pueblos_noticias_200'

    def get_categorias_string(self):
        categorias = []
        # noticia = PueblosNoticias.objects.get(id=noticia200.noticia)
        pueblosNc = PueblosNc.objects.filter(noticia=self.noticia)
        for puebloNc in pueblosNc:
            categoria = PueblosCategoriasSemandal.objects.get(id=puebloNc.categoria.id)
            # print categoria.dscategoria
            categorias.append(categoria.dscategoria)
        return categorias

    def get_categorias_id(self):
        categorias = []
        # noticia = PueblosNoticias.objects.get(id=noticia200.noticia)
        pueblosNc = PueblosNc.objects.filter(noticia=self.noticia)
        for puebloNc in pueblosNc:
            categoria = PueblosCategoriasSemandal.objects.get(id=puebloNc.categoria.id)
            # print categoria.dscategoria
            categorias.append(categoria.id)
        return categorias


# Tabla relacion n a n de Noticias_200 y Palabras


class PueblosNoticiasPalabras(models.Model):
    noticia_200 = models.ForeignKey('PueblosNoticias200', on_delete=models.CASCADE)
    palabra = models.CharField(unique=False, max_length=100)

    class Meta:
        managed = True
        db_table = 'pueblos_noticias_palabras'
        unique_together = (('noticia_200', 'palabra'),)

    def get_categorias_id_all(self):
        categorias = []
        palabras = PueblosNoticiasPalabras.objects.filter(palabra=self.palabra)
        for palabra in palabras:
            # print '______________________________________' + palabra.palabra
            noticia200 = PueblosNoticias200.objects.get(id=palabra.noticia_200.id)
            # noticia = PueblosNoticias.objects.get(id=noticia200.noticia)
            pueblosNc = PueblosNc.objects.filter(noticia=noticia200.noticia)
            for puebloNc in pueblosNc:
                categoria = PueblosCategoriasSemandal.objects.get(id=puebloNc.categoria.id)
                categorias.append(categoria.id)
        return categorias

    def get_categorias_string_all(self):
        categorias = []
        palabras = PueblosNoticiasPalabras.objects.filter(palabra=self.palabra)
        for palabra in palabras:
            # print '______________________________________' + palabra.palabra
            noticia200 = PueblosNoticias200.objects.get(id=palabra.noticia_200.id)
            # noticia = PueblosNoticias.objects.get(id=noticia200.noticia)
            pueblosNc = PueblosNc.objects.filter(noticia=noticia200.noticia)
            for puebloNc in pueblosNc:
                categoria = PueblosCategoriasSemandal.objects.get(id=puebloNc.categoria.id)
                categorias.append(categoria.dscategoria)
        return categorias

    def get_categorias_string(self):
        categorias = []
        noticia200 = PueblosNoticias200.objects.get(id=self.noticia_200.id)
        # noticia = PueblosNoticias.objects.get(id=noticia200.noticia)
        pueblosNc = PueblosNc.objects.filter(noticia=noticia200.noticia)
        for puebloNc in pueblosNc:
            categoria = PueblosCategoriasSemandal.objects.get(id=puebloNc.categoria.id)
            # print categoria.dscategoria
            categorias.append(categoria.dscategoria)
        return categorias

    def get_categorias_id(self):
        categorias = []
        noticia200 = PueblosNoticias200.objects.get(id=self.noticia_200.id)
        # noticia = PueblosNoticias.objects.get(id=noticia200.noticia)
        pueblosNc = PueblosNc.objects.filter(noticia=noticia200.noticia)
        for puebloNc in pueblosNc:
            categoria = PueblosCategoriasSemandal.objects.get(id=puebloNc.categoria.id)
            categorias.append(categoria.id)
        return categorias

    def get_indice(self, id_categoria):
        indice = float(0)
        categorias = self.get_categorias_id()
        nom_cat = self.get_categorias_string()
        repeticiones = PueblosNoticiasPalabras.objects.filter(palabra=self.palabra)
        # print 'La palabra ' + self.palabra + ' aparece ' + str(len(repeticiones)) + ' veces en la db'
        for categoria in categorias:
            if id_categoria == categoria:
                indice += 1
        # print 'valor indice antes return ' + str(indice)
        # print 'tamanio categorias ' + str(len(categorias))
        indice /= len(repeticiones)
        # print 'tamanio indice ' + str(float(indice))
        return indice


class PueblosNoticiaCategorizada(models.Model):
    # coger con objeto.labels.all() equivale a objeto.label_set.objects.all() ##imvu i am virtual user
    noticia = models.ForeignKey('PueblosNoticias')
    categorias_sugeridas = models.ForeignKey('PueblosCategoriasSemandal', related_name='suggested_labels')
    comprobado = models.CharField(max_length=1, default='0')

    class Meta:
        managed = True
        db_table = 'pueblos_noticia_categorizada'


class PueblosRule(models.Model):
    r_id = models.AutoField(auto_created=True, primary_key=True, default=1)
    support = models.IntegerField(default=0)
    confidence = models.FloatField(default=0.0)

    class Meta:
        managed = True
        db_table = 'rule'


class PueblosConclusion(models.Model):
    c_id = models.AutoField(auto_created=True, primary_key=True, default=1)
    c_word = models.CharField(max_length=60)
    r = models.ForeignKey('PueblosRule', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'conclusion'


class PueblosPremise(models.Model):
    p_id = models.AutoField(auto_created=True, primary_key=True, default=1)
    p_word = models.CharField(max_length=60)
    r = models.ForeignKey('PueblosRule', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'premise'


class PueblosDiccionarioSintactico(models.Model):
    word = models.CharField(max_length=60, unique=True)
    replace_word = models.CharField(max_length=60, blank=True)

    def __unicode__(self):
        return self.word

    def __str__(self):
        return unicode(self).encode('utf-8')

    class Meta:
        managed = True
        db_table = 'pueblos_diccionario_sintactico'


class PueblosNoticiasTest(models.Model):
    # referencia noticia para poder ver sus categorias en PueblosNc
    noticia = models.ForeignKey('PueblosNoticias', on_delete=models.CASCADE)
    dstitular = models.TextField(max_length=1500, blank=True, null=True)
    dscuerpo = models.TextField(max_length=50000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pueblos_noticias_test'

    def get_categorias_string(self):
        categorias = []
        pueblos_nc = PueblosNc.objects.filter(noticia=self.noticia)
        for pueblo_nc in pueblos_nc:
            categoria = PueblosCategoriasSemandal.objects.get(id=pueblo_nc.categoria.id)
            # print categoria.dscategoria
            categorias.append(categoria.dscategoria)
        return categorias

    def get_categorias_id(self):
        categorias = []
        # noticia = PueblosNoticias.objects.get(id=noticia200.noticia)
        pueblos_nc = PueblosNc.objects.filter(noticia=self.noticia)
        for pueblo_nc in pueblos_nc:
            categoria = PueblosCategoriasSemandal.objects.get(id=pueblo_nc.categoria.id)
            # print categoria.dscategoria
            categorias.append(categoria.id)
        return categorias


class PueblosNoticiasTestCategorias(models.Model):
    noticia_test = models.ForeignKey('PueblosNoticiasTest', on_delete=models.CASCADE)
    categorias_sugeridas = models.CharField(max_length=80, blank=False)
    regla = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        managed = True
        db_table = 'pueblos_noticias_test_categorias'


class PueblosTestCase(models.Model):
    n_news = models.IntegerField(default=1)
    n_news_test = models.IntegerField(default=1)
    limit = models.IntegerField(default=10)
    use_syn_dict = models.BooleanField(default=False)
    confidence = models.FloatField(default=0.8)
    support = models.FloatField(default=0.5)
    state = models.CharField(max_length=60, blank=True, default='not done')

    class Meta:
        managed = True
        db_table = 'pueblos_test_case'
"""
    Fin tabla generada para pruebas y FCA
"""


class PueblosNvistas(models.Model):
    noticia = models.ForeignKey('PueblosNoticias', models.DO_NOTHING)
    usuario = models.ForeignKey('PueblosUsuario', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pueblos_nvistas'
        unique_together = (('usuario', 'noticia'),)


class PueblosProvincia(models.Model):
    dsprovincia = models.CharField(unique=True, max_length=200)
    dspopcional = models.CharField(unique=True, max_length=200, blank=True, null=True)
    bprov = models.CharField(unique=True, max_length=200)
    bprovop = models.CharField(unique=True, max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pueblos_provincia'


class PueblosPueblo(models.Model):
    dspueblo = models.CharField(max_length=200)
    dsopcional = models.CharField(max_length=200)
    cp = models.IntegerField()
    latitud = models.DecimalField(max_digits=11, decimal_places=7, blank=True, null=True)
    longitud = models.DecimalField(max_digits=11, decimal_places=7, blank=True, null=True)
    busqueda = models.CharField(max_length=200)
    busquedaop = models.CharField(max_length=200)
    url = models.CharField(max_length=200, blank=True, null=True)
    opencms = models.IntegerField()
    redirec = models.CharField(max_length=200, blank=True, null=True)
    provincia_id = models.IntegerField()
    habitantes = models.IntegerField(blank=True, null=True)
    deuda = models.FloatField(blank=True, null=True)
    deudaxhab = models.DecimalField(max_digits=11, decimal_places=7, blank=True, null=True)
    densidad = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    superficie = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    fecha_ins = models.DateField()
    wiki = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'pueblos_pueblo'


class PueblosPuebloInfoextra(models.Model):
    pueblo_id = models.IntegerField()
    contrato_temp = models.IntegerField()
    contrato_indef = models.IntegerField()
    url_datos = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'pueblos_pueblo_infoextra'


class PueblosReglasOntologia(models.Model):
    etiqueta_id = models.IntegerField()
    subcategoria_de_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pueblos_reglas_ontologia'
        unique_together = (('etiqueta_id', 'subcategoria_de_id'),)


class PueblosSigp(models.Model):
    id_user_id = models.IntegerField()
    id_p_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pueblos_sigp'
        unique_together = (('id_user_id', 'id_p_id'),)


class PueblosStatus(models.Model):
    dsstatus = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'pueblos_status'


class PueblosTLiked(models.Model):
    id_user_id = models.IntegerField()
    id_n_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pueblos_t_liked'
        unique_together = (('id_user_id', 'id_n_id'),)


class PueblosUsuario(models.Model):
    dsusuario = models.CharField(unique=True, max_length=100)
    dsnombre = models.CharField(max_length=100)
    dsapellido1 = models.CharField(max_length=100)
    dsapellido2 = models.CharField(max_length=100)
    pueblo_id = models.IntegerField()
    token = models.CharField(max_length=200)
    correo = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pueblos_usuario'


class PueblosVecinos(models.Model):
    id1_id = models.IntegerField()
    id2_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pueblos_vecinos'


class PueblosVersions(models.Model):
    tabla = models.CharField(max_length=20)
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pueblos_versions'


class PueblosVotaciones(models.Model):
    id_n_id = models.IntegerField()
    id_user_id = models.IntegerField()
    categoria_id = models.IntegerField()
    votacion = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pueblos_votaciones'
        unique_together = (('id_n_id', 'id_user_id', 'categoria_id'),)
