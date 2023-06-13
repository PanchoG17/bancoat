from django.contrib import admin

from django.http import HttpResponse

from apps.electrodependientes.models import Diagnostico, Electrodependiente, Medico, TitularDeSuministro
#from apps.banco.models import AyudaTecnica

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime

class TitularSuministroInline(admin.TabularInline):
    model = TitularDeSuministro
    extra = 0

class DiagnosticoInline(admin.StackedInline):
    model = Diagnostico
    extra = 0

class ElectrodependienteAdmin(admin.ModelAdmin):
    inlines = (TitularSuministroInline, DiagnosticoInline)
    list_display = ( 'persona_electrodependiente', 'us', 'rupe', 'pension_nacional', 'activo' )
    list_filter = ( 'persona_electrodependiente' , 'activo' )
    search_fields = [ 'persona_electrodependiente' ]
    actions = [ 'generar_reporte_electrodependiente']
    ordering = [ 'persona_electrodependiente' ]

    # def generar_reporte_electrodependiente(self, request, queryset):
    #     response = HttpResponse(content_type='application/pdf')
    #     response['Content-Disposition'] = 'attachment: filename="electrodependiente.pdf"'

    #     for electro in queryset:
    #         print(electro)

    #         p = canvas.Canvas(response)

    #         p.showPage()
    #         p.save()

    #         return response

# admin.site.register(Electrodependiente, ElectrodependienteAdmin)
# admin.site.register(TitularDeSuministro)
# admin.site.register(Medico)


