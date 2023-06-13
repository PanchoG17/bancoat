from . import views
from django.urls import path
from apps.persona.views import *

app_name = 'persona'

urlpatterns = [

    path( 'registrar', registrarPersona, name = 'registrar_persona'),
    path( 'baja', setBajaPersona, name = 'baja_persona'),
    path( 'listado', personaListView.as_view(), name = 'listado_persona'),
    path( 'detalle/<int:pk>', personaDetailView.as_view(), name = 'detalle_persona'),

    path( 'beneficiario/registrar', registrarBeneficiario, name = 'registrar_beneficiario'),
    path( 'beneficiario/editar', editarBeneficiario, name = 'editar_beneficiario'),
    path( 'beneficiario/listado', beneficiarioListView.as_view(), name = 'listado_beneficiario'),
    path( 'beneficiario/detalle/<int:pk>', beneficiarioDetailView.as_view(), name = 'detalle_beneficiario'),

]