from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

from ckeditor.fields import RichTextField
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField

from apps.localizacion.models import Localidad, Provincia, Barrio, Pais

class Base(models.Model):
    fecha_creacion= models.DateTimeField(auto_now_add= True, blank= True, null=True)
    fecha_modificacion= models.DateTimeField(auto_now= True, blank=True, null=True)
    fecha_baja = models.DateTimeField(editable=False, blank=True, null=True)

    activo= models.BooleanField(editable=False, default= True, verbose_name= 'Activo')

    class Meta:
        abstract= True

class General(Base):

    titulo= models.CharField(max_length= 200, verbose_name= 'Titulo', unique=True)
    descripcion= models.TextField(verbose_name= 'Descripción', blank= True, null= True)

    usuario_creador= models.ForeignKey(User, on_delete=models.CASCADE)
    usuario_modificacion = models.IntegerField(blank=True,null=True,editable=False)
    usuario_baja = models.IntegerField(blank=True,null=True,editable=False)

    def save(self, *args, **kwargs):
        if self.titulo:        
            self.titulo = self.titulo.capitalize()
        super().save(*args, **kwargs)

    class Meta:
        abstract= True

class Contacto(models.Model):

    codigo_area_c = models.CharField(verbose_name='Cód. de área celular', max_length=5, blank=False, null=False)
    numero_telefono_c = models.CharField(verbose_name='Nro. de celular', max_length=7, blank=False, null=False)
    codigo_area_f = models.CharField(verbose_name='Cód. de área teléfono fijo', max_length=5, blank=True, null=True)
    numero_telefono_f = models.CharField(verbose_name='Nro. de teléfono fijo', max_length=7, blank=True, null=True)

    email = models.EmailField(verbose_name='E-mail de contacto', blank=False, null=False)

    class Meta:
        abstract= True

class Ubicacion(models.Model):

    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE)
    calle = models.CharField(verbose_name='Calle', max_length=100, blank=True, null=True)
    numero = models.CharField(verbose_name='Altura calle', max_length=5, blank=True, null=True)

    class Meta:
        abstract= True

class UbicacionDetallada(Ubicacion):

    ZONAS = (('R', 'RURAL'),('U', 'URBANA'),('M', 'MIXTA'))
    zona = models.CharField(verbose_name='Zona',choices=ZONAS,max_length=1)

    tipo_vivienda = models.ForeignKey('clasificadores.TipoVivienda',verbose_name='Tipo de vivienda',on_delete=models.CASCADE)

    nacionalidad = models.ForeignKey(Pais,verbose_name='Nacionalidad',on_delete=models.CASCADE)
    provincia = models.ForeignKey(Provincia,verbose_name='Provincia',on_delete=models.CASCADE)
    localidad = ChainedForeignKey(Localidad,chained_field='provincia',chained_model_field='provincia')
    #barrio = ChainedForeignKey(Barrio,chained_field='localidad',chained_model_field='localidad')
    barrio = models.CharField(verbose_name='Barrio',max_length=25,blank=True,null= True)

    numero_departamento = models.CharField(verbose_name='Numero de departamento',max_length=5,blank=True,null= True)
    tira = models.CharField(verbose_name='Numero de tira',max_length=5,blank=True,null= True)
    numero_piso = models.CharField(verbose_name='Numero de piso',max_length=5,blank=True,null= True)

    lote = models.CharField(verbose_name='Numero de lote',max_length=5,blank=True,null= True)
    macizo = models.CharField(verbose_name='Numero de macizo',max_length=5,blank=True,null= True)
    manzana = models.CharField(verbose_name='Numero de manzana',max_length=5,blank=True,null= True)
    parcela = models.CharField(verbose_name='Numero de parcela',max_length=5,blank=True,null= True)
    seccion = models.CharField(verbose_name='Numero de sección',max_length=5,blank=True,null= True)

    class Meta:
        abstract= True