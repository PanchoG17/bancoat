from django.contrib import admin
from apps.localizacion.models import Pais, Provincia, Localidad, Barrio

admin.site.site_header = 'SGD | Sitio de administración BaPTA (Banco de productos y tecnologías de apoyo.)'

class PaisAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_alfa2', 'codigo_alfa3', 'codigo_numerico')#, 'bandera')
    search_fields = ['nombre']
    ordering = ['nombre']

admin.site.register(Pais, PaisAdmin)

class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'region', 'pais')
    search_fields = ['nombre']
    ordering = ['nombre']

admin.site.register(Provincia, ProvinciaAdmin)

class LocalidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_postal', 'zona', 'activo')
    search_fields = ['nombre']
    ordering = ['nombre']

admin.site.register(Localidad, LocalidadAdmin)

class BarrioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'localidad','zona', 'activo')
    search_fields = ['nombre']
    ordering = ['nombre']

admin.site.register(Barrio, BarrioAdmin)