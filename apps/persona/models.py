from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import int_list_validator

from apps.clasificadores.models import Base, General, Contacto, UbicacionDetallada, EstadoCivil, TipoDiscapacidad, TipoDocumento,TipoParentesco, Genero, ObraSocial

FALSE_TRUE = ((True,'SI'),(False,'NO'))

class Persona(General, Contacto, UbicacionDetallada):

    ### Choices del modelo ###
    TIPO_DNI = (('DU','Documento Único'),('LC','Libreta Cívica'))

    ### Atributos del modelo ###
    documento = models.PositiveIntegerField(verbose_name='Numero de documento',blank=False,null=False,unique=True)
    documento_tipo = models.CharField(verbose_name='Tipo de documento',choices=TIPO_DNI,max_length=2)
    cuit = models.CharField(verbose_name='CUIT / CUIL',blank=True,null=True,unique=True, max_length=15)
    nombre = models.CharField(verbose_name='Nombre',null=False,blank=False,max_length=50)
    apellido = models.CharField(verbose_name='Apellido',null=False,blank=False,max_length=50)
    genero = models.ForeignKey(Genero, verbose_name=("Genero"), on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento',null=True,blank=True)
    estado_civil = models.ForeignKey(EstadoCivil,verbose_name='Estado civíl',on_delete=models.CASCADE)

    email = models.EmailField(verbose_name='E-mail de contacto', blank=True, null=True)
    titulo= None
    descripcion= None

    class Meta:
        db_table = 'persona'
        verbose_name = 'Persona'
        verbose_name_plural = ' Personas'
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.capitalize()
        self.apellido = self.apellido.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}".format( self.nombre +' '+ self.apellido + ' - ' + str(self.documento))

    def get_absolute_url(self):
        return reverse('persona:detalle_persona', kwargs={'pk' : self.pk})

    def getTelefono(self):
        if self.codigo_area_c and self.numero_telefono_c:
            return self.codigo_area_c + self.numero_telefono_c
        else:
            return self.codigo_area_f + self.numero_telefono_f

    def getDireccion(self):
        if self.calle and self.numero:
            if self.numero_departamento:
                return self.calle + " " + self.numero + ", Departamento " + self.numero_departamento
            else:
                return self.calle + " " + self.numero

        if self.tira:
            return "Tira " + self.tira + ", Piso " + self.numero_piso + ", Departamento " + self.numero_departamento

        if self.lote:
            return "Lote " + self.lote + ", Manzana " + self.manzana + ", Parcela " + self.parcela

class Beneficiario(General):

    persona_beneficiaria = models.OneToOneField( Persona, verbose_name='Beneficiario', on_delete=models.CASCADE, unique=True, null=False , blank=False, related_name="beneficiario")
    persona_responsable = models.OneToOneField( Persona, verbose_name='Responsable', on_delete=models.CASCADE,null=False , blank=False, related_name="responsable")
    vinculo = models.ForeignKey(TipoParentesco, on_delete=models.CASCADE)
    discapacidad = models.ForeignKey(TipoDiscapacidad,verbose_name='Discapadidad',on_delete=models.CASCADE,blank=False,null=False)
    permanente = models.BooleanField(verbose_name='¿Es permanente la discapacidad?',choices=FALSE_TRUE,max_length=2,blank=True,null=True)

    cud = models.BooleanField(verbose_name='CUD', choices=FALSE_TRUE)
    fecha_vencimiento_cud = models.DateField(verbose_name='Fecha de vencimiento CUD',blank=True,null=True)
    archivo_cud = models.ImageField(verbose_name='Adjuntar CUD', upload_to='documentacion/beneficiarios/',blank=True,null=True)

    obra_social = models.ForeignKey(ObraSocial,verbose_name='Obra social',on_delete=models.CASCADE,blank=True,null=True)
    nro_afiliado = models.CharField(verbose_name='Numero de afiliado', max_length=25,blank=True,null=True,unique=True)

    descripcion = None
    titulo = None

    class Meta:
        db_table = 'beneficiario'
        verbose_name = 'Beneficiario'
        verbose_name_plural = 'Beneficiarios'
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.persona_beneficiaria)

"""
    Con respecto a la documentación: el beneficiario tendrá asociada documentación para su legajo individual.
"""
class DocumentacionBeneficiario(Base):

    beneficiario = models.ForeignKey(Beneficiario, verbose_name='Beneficiario', on_delete=models.CASCADE, editable= False, blank=True, null=True)
    tipo_documento = models.ForeignKey(TipoDocumento, verbose_name='Tipo de documento', on_delete=models.CASCADE)
    archivo = models.FileField(verbose_name='Adjuntar documentación', upload_to='documentacion/beneficiarios/')
    descripcion= models.CharField(verbose_name= 'Descripción', blank= False, null= False, max_length=80)

    class Meta:
        unique_together = [['beneficiario','tipo_documento', 'archivo']]
        db_table = 'documentacion_beneficiario'
        verbose_name = 'Documentación de Beneficiario'
        verbose_name_plural = 'Documentación de Beneficiarios'
        ordering = ['id']

    def __str__(self):
        return "Beneficiario"