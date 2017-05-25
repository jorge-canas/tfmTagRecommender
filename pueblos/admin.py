from django.contrib import admin

# Register your models here.
from .models import *


class PueblosDiccionarioSintacticoAdmin(admin.ModelAdmin):
    search_fields = ['word']

admin.site.register(PueblosNoticias)
admin.site.register(PueblosNoticiaCategorizada)
admin.site.register(PueblosTestCase)
admin.site.register(PueblosCategoria)
admin.site.register(PueblosDiccionarioSintactico, PueblosDiccionarioSintacticoAdmin)
admin.site.register(PueblosNc)
admin.site.register(PueblosPueblo)
admin.site.register(PueblosNoticias200)
admin.site.register(PueblosNoticiasTest)
admin.site.register(PueblosNoticiasTestCategorias)
