from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from apps.abstract import Base, General, Contacto
from apps.persona.models import Persona
from apps.clasificadores.models import TipoParentesco, Empresa

# CHOICES
FALSE_TRUE = ((True,'SI'),(False,'NO'))
TIEMPOREQUERIDO = (('6', 'Hasta 6 meses'),('12', 'Hasta 1 año'),('24', 'Hasta 2 años'))

"""
Con respecto al electrodependiente, este podrá ser o no un beneficiario
"""
class Electrodependiente(General):
    persona_electrodependiente = models.OneToOneField(Persona,verbose_name='Persona',on_delete=models.CASCADE)
    nro_expediente = models.PositiveIntegerField(verbose_name='Expediente número',blank=True,null=True)
    letra_expediente = models.CharField(verbose_name='Expediente letra', max_length=2, blank=True, null=True)
    anio_expediente = models.PositiveIntegerField(verbose_name='Expediente año',blank=True,null=True)
    us = models.BooleanField(verbose_name='U.S', choices=FALSE_TRUE)
    rupe = models.BooleanField(verbose_name='RUPE', choices=FALSE_TRUE)
    pension_nacional = models.BooleanField(verbose_name='Pensión Nacional', choices=FALSE_TRUE)
    cud = models.BooleanField(verbose_name='CUD', choices=FALSE_TRUE)
    fecha_vencimiento_cud = models.DateField(verbose_name='Fecha de vencimiento CUD',blank=True,null=True)

    titulo= None
    descripcion= None

    class Meta:
        db_table = 'electrodependiente'
        verbose_name = 'Persona Electrodependiente'
        verbose_name_plural = ' Electrodependientes'
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.persona_electrodependiente)

class DocumentacionElectro(models.Model):
    electrodependiente = models.ForeignKey(Electrodependiente, verbose_name='Electrodependiente', on_delete=models.CASCADE, blank=False, null=False)
    documentacion = models.FileField(verbose_name='Adjuntar documentación (Max. 5 archivos)', upload_to='documentacion/electrodependientes/', blank= True, null= True)
    formulario = models.FileField(verbose_name='Adjuntar Formulario físico', upload_to='documentacion/electrodependientes/',blank=True,null=True)

    class Meta:
        db_table = 'documentacion_electro'
        verbose_name = 'Documentacion electrodependiente'
        verbose_name_plural = 'Documentacion electrodependientes'
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.electrodependiente)


class TitularDeSuministro(General):
    electrodependiente = models.ForeignKey(Electrodependiente, verbose_name='Electrodependiente', on_delete=models.CASCADE, blank=False, null=False)
    titularServicio = models.ForeignKey(Persona, verbose_name='Titular del servicio eléctrico', on_delete=models.CASCADE, blank=False, null=False)
    vinculo = models.ForeignKey(TipoParentesco, on_delete=models.CASCADE, verbose_name="Vinculo con la persona solicitante", blank=False, null=False)
    proveedor_suministro = models.ForeignKey(Empresa, verbose_name='Compañía proveedora del suministro', on_delete=models.CASCADE, blank=False, null=False)
    numero_cliente = models.CharField(verbose_name='Número de cliente', max_length=20, blank=False, null=False)
    titulo= None
    descripcion= None

    class Meta:
        db_table = 'titular_de_suministro'
        verbose_name = 'Titular de suministro'
        verbose_name_plural = 'Titulares de suministros'
        ordering = ['id']

    def __str__(self):
        return "{}".format( self.titularServicio )

"""
Con respecto al médico, este tendrá uno o más diagnósticos
"""
class Medico(General, Contacto):

    TIPO_DNI = (('DU','Documento Único'),('LC','Libreta Cívica'))

    ### Atributos del modelo ###

    # persona = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name='Persona')
    # documento_tipo = models.CharField(verbose_name='Tipo de documento',choices=TIPO_DNI,max_length=2)

    nombre = models.CharField(verbose_name='Nombres',null=False,blank=False,max_length=50)
    apellido = models.CharField(verbose_name='Apellidos',null=False,blank=False,max_length=50)
    documento = models.PositiveIntegerField(verbose_name='Numero de documento',blank=False,null=False,unique=True)

    matricula_profesional = models.CharField(verbose_name='Matrícula profesional', max_length=10, blank=False, null=False)
    codigo_area_c = models.CharField(verbose_name='Cód. de área celular', max_length=5, blank=True, null=True)
    numero_telefono_c = models.CharField(verbose_name='Nro. de celular', max_length=7, blank=True, null=True)

    descripcion = None
    titulo = None

    class Meta:
        db_table = 'medico'
        verbose_name = 'Médico'
        verbose_name_plural = ' Médicos'
        ordering = ['id']

    def __str__(self):
        return "{} {} - {}".format( self.nombre, self.apellido, self.matricula_profesional )

class Diagnostico(Base):

    electrodependiente = models.ForeignKey(Electrodependiente,verbose_name='Electrodependiente',on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico,on_delete=models.CASCADE)
    historia_clinica = models.TextField(blank=True,null=True,verbose_name='Resumen detallado de la historia clínica')
    diagnostico = models.TextField(blank=True,null=True, verbose_name="Diagnóstico CIE10")
    tiempo_requerido =  models.CharField(verbose_name='Tiempo estimado de requerimiento',choices=TIEMPOREQUERIDO,max_length=2)
    fecha_diagnostico = models.DateField(verbose_name='Fecha de diagnóstico',default=now)
    fecha_finalizacion = models.DateField(verbose_name='Fecha de finalización', editable=False)

    equipo_dialisis = models.BooleanField(verbose_name='Diálisis peritoneal automatizada (DPA) domiciliaria',default=False, choices=FALSE_TRUE)
    equipo_alimentacion = models.BooleanField(verbose_name='Bomba de infusión contínua, bomba de alimentación enteral o parenteral',default=False, choices=FALSE_TRUE)
    equipo_ventilacion = models.TextField(verbose_name='Equipos relacionados al soporte de la ventilación',blank=True,null=True)
    otro = models.TextField(verbose_name='Otros',blank=True,null=True)

    class Meta:
        db_table = 'diagnostico'
        verbose_name = 'Diagnóstico'
        verbose_name_plural = 'Diagnósticos'
        ordering = ['id']

    def __str__(self):
        return "{}".format( self.medico )

    def save(self):
        self.fecha_finalizacion = self.fecha_diagnostico + relativedelta(months=+int(self.tiempo_requerido))
        super(Diagnostico, self).save()
