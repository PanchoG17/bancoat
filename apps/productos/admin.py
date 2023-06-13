from django.contrib import admin

from apps.productos.models import ProductoBaja

class ProductoBajaAdmin(admin.ModelAdmin):
    list_display = (
        'producto',
        'motivo_baja',
        'fecha_baja',
        'usuario_baja'
    )

# Register your models here.
admin.site.register(ProductoBaja,ProductoBajaAdmin)


