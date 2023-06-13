from django.contrib import admin

from apps.persona.models import Beneficiario, Persona, DocumentacionBeneficiario

class PersonaAdmin(admin.ModelAdmin):

    fields= (
        # Datos
        'nombre','apellido','documento_tipo','documento','cuit','fecha_nacimiento','estado_civil','genero',

        #Contacto
        'codigo_area_c','numero_telefono_c','codigo_area_f','numero_telefono_f','email',

        # Ubicacion detallada
        'nacionalidad','provincia','localidad','zona','barrio','calle','numero','tira','numero_piso','numero_departamento','lote','macizo','parcela','seccion',

        # General
        'usuario_creador'
    )

    list_display = ( 'documento', 'apellido', 'nombre','nacionalidad', 'localidad')
    list_filter = ( 'documento', 'apellido', 'nombre')
    search_fields = [ 'documento', 'apellido', 'nombre' ]
    ordering = [ 'apellido' ]

class DocumentacionInline(admin.TabularInline):
    model = DocumentacionBeneficiario
    extra = 1

class BeneficiarioAdmin(admin.ModelAdmin):
    inlines = (DocumentacionInline,)
    list_display = (
        'persona_beneficiaria',
        'persona_responsable',
        'discapacidad'
    )
    list_filter = (
        'persona_beneficiaria',
        'discapacidad'
    )
    search_fields = [
        'persona_beneficiaria',
        'persona_responsable',
        'discapacidad'
    ]
    ordering = [
        'persona_beneficiaria'
    ]

# admin.site.register(Persona, PersonaAdmin)
# admin.site.register(Beneficiario, BeneficiarioAdmin)