from django.contrib import admin

from apps.inventario.models import TipoComprobante, PuntoVenta, Kardex, Numerador
from apps.inventario.models import Comprobante, DetalleEntrada, DetallePrestamo, DetalleDevolucion

# Register your models here.
class DetalleEntradaInLine(admin.TabularInline):
    model = DetalleEntrada
    extra = 0
    min_num = 1

class DetallePrestamoInLine(admin.TabularInline):
    model = DetallePrestamo
    extra = 0
    min_num = 1

class DetalleDevolucionInLine(admin.TabularInline):
    model = DetalleDevolucion
    extra = 0
    min_num = 1

class ComprobanteAdmin(admin.ModelAdmin):
    list_display = ('tipo_comprobante','get_codigo','punto_venta','fecha_operacion','descripcion')

    search_fields = ['tipo_comprobante__descripcion','punto_venta__titulo','descripcion']

    inlines = [DetalleEntradaInLine,DetallePrestamoInLine,DetalleDevolucionInLine]

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.id > 1:
            return False
        return super().has_change_permission(request, obj=obj)


    @admin.display(ordering='tipo_comprobante__codigo', description='Numero de comprobante')
    def get_codigo(self, obj):
        return obj.tipo_comprobante.codigo + ' ' + obj.punto_venta.codigo + '-' + str(obj.numero).zfill(6)

class KardexAdmin(admin.ModelAdmin):
    list_display = ('get_numero_comprobante', 'sucursal', 'fecha_operacion', 'articulo', 'cantidad_ingreso', 'cantidad_salida', 'cantidad_total')

    @admin.display(ordering='tipo_comprobante__codigo', description='Numero de comprobante')
    def get_numero_comprobante(self, obj):
        return obj.comprobante.tipo_comprobante.codigo + ' ' + obj.comprobante.punto_venta.codigo + '-' + str(obj.comprobante.numero).zfill(6)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.id > 1:
            return False
        return super().has_change_permission(request, obj=obj)


# admin.site.register(Comprobante, ComprobanteAdmin)
# admin.site.register(Kardex, KardexAdmin)
# admin.site.register(TipoComprobante)
# admin.site.register(PuntoVenta)
# admin.site.register(Numerador)
