from django.contrib import admin

from apps.clasificadores.models import EstadoCivil, TipoDiscapacidad, TipoDocumento,TipoParentesco,TipoVivienda, TipoBaja, Empresa, Sucursal, Genero, ObraSocial
from apps.inventario.models import Kardex

class EmpresaAdmin(admin.ModelAdmin):

    fields= (
        # General
        'titulo','descripcion','tipo_servicio','razon_social','cuit','ingresos_brutos',

        # Contacto
        'codigo_area_c','numero_telefono_c','codigo_area_f','numero_telefono_f','email','sitio_web',

        # Ubicacion
        'pais','provincia','localidad','calle','numero',

        'usuario_creador'
    )

    list_display = ( 'titulo', 'tipo_servicio', 'cuit','razon_social', 'localidad')
    list_filter = ( 'tipo_servicio', 'razon_social')

class SucursalAdmin(admin.ModelAdmin):

    fields= (

        # General
        'titulo','descripcion','is_central',
        # Contacto
        'codigo_area_c','numero_telefono_c','codigo_area_f','numero_telefono_f','email',
        # Ubicacion
        'provincia','localidad','calle','numero',
        'usuario_creador'
    )

    list_display = ( 'titulo', 'get_productos')

    # Contador de productos por sucursal
    @admin.display(description='Productos en sucursal')
    def get_productos(self, obj):
        total = 0
        for i in range(1,15):
            try:
                kardex = Kardex.objects.filter( sucursal = obj.id, articulo= i ).last()
                total += kardex.cantidad_total
            except:
                pass

        return total

admin.site.register(Empresa,EmpresaAdmin)
admin.site.register(Sucursal,SucursalAdmin)
admin.site.register(ObraSocial)
admin.site.register(EstadoCivil)
admin.site.register(TipoDiscapacidad)
admin.site.register(TipoDocumento)
admin.site.register(TipoParentesco)
admin.site.register(Genero)
admin.site.register(TipoVivienda)
admin.site.register(TipoBaja)