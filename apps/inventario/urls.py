from . import views
from django.urls import path
from apps.inventario.views import *

app_name = 'inventario'

urlpatterns = [

    path( 'comprobantes/crear', newComprobante, name = 'crear_comprobante'),
    path( 'comprobantes/historial', historialComprobantes, name = 'historial_comprobantes'),
    path( 'comprobantes/print/<str:numero>', printComprobante, name = 'print_comprobante'),
    path( 'kardex', KardexListView.as_view(), name = 'kardex')

]