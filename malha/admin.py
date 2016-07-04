from django.contrib import admin
from malha.models import *


# Register your models here.
@admin.register(Linha)
class LinhaAdmin(admin.ModelAdmin):
    fields = ('label', 'nome')


@admin.register(Parada)
class ParadaAdmin(admin.ModelAdmin):
    fields = ('label', 'nome')


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    fields = ('linha', 'secret_key')
