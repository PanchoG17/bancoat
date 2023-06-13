from django.contrib.auth.decorators import login_required
from django.urls import path
from apps.electrodependientes.views import *

app_name = 'electrodependientes'

urlpatterns = [

    path( 'registrar', registrarElectro, name = 'registrar_electro'),
    path( 'editar', editarElectro, name = 'editar_electro'),
    path( 'listado', electroListView.as_view(), name = 'listado_electro'),
    path( 'detalle/<int:pk>', electroDetailView.as_view(), name = 'detalle_electro'),

    path( 'medico/registrar', registrarMedico, name = 'registrar_medico'),
    path( 'medico/listado', medicoListView.as_view(), name = 'listado_medico'),

]