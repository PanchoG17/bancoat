from django.contrib import admin
from django.db import models
from datetime import datetime

class Pais(models.Model):
    nombre = models.CharField('Nombre de País',max_length=50,blank=False)
    codigo_alfa2 = models.CharField('Código Alfa 2',max_length=2,blank=True, null=True)
    codigo_alfa3 = models.CharField('Código Alfa 3',max_length=3,blank=True, null=True)
    codigo_numerico = models.IntegerField('Código Numérico',blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField('Activo', blank=True, default=True)

    #MataDatos
    class Meta:
        db_table = 'pais'
        verbose_name = 'País'
        verbose_name_plural = '  Paises'
        ordering = ['nombre']

    #Métodos
    def __str__(self):
        return self.nombre

class Provincia(models.Model):

    REGIONES = (
        (0, 'ESTE'),
        (1, 'OESTE'),
        (2, 'NORTE'),
        (3, 'SUR'),
        (4, 'NORESTE'),
        (5, 'SURESTE'),
        (6, 'NOROESTE'),
        (7, 'SUROESTE'),
        (8, 'CENTRO'),
        (9, 'CENTROESTE'),
        (10, 'CENTROOESTE'),
        (11, 'CENTRONORTE'),
        (12, 'CENTROSUR')
    )

    pais = models.ForeignKey( Pais,on_delete=models.PROTECT)
    nombre = models.CharField('Nombre de Provincia',max_length=50,blank=False)
    codigo = models.CharField('Código de Provincia',max_length=4,blank=False)
    region = models.IntegerField('Zona Geográfica:',choices=REGIONES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField('Activo',blank=True,default=True)

    #MetaDatos
    class Meta:
        db_table = 'provincia'
        verbose_name = 'Provincia'
        verbose_name_plural = '  Provincias'
        ordering = ['nombre']

    #Métodos
    def __str__(self):
        return "{}".format( self.nombre )

class Localidad(models.Model):

    #Choices
    ZONAS = ((0, 'Centro'),(1, 'Norte'),(2, 'Sur'))

    provincia = models.ForeignKey( Provincia, on_delete=models.PROTECT )
    codigo_postal = models.CharField('Código Postal', max_length=6, blank = False)
    nombre = models.CharField('Nombre',max_length=20,blank = False)
    zona = models.IntegerField('Zona',choices=ZONAS)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField('Activa',blank=True,default=True)

    #MetaDatos
    class Meta:
        db_table = 'localidad'
        verbose_name = 'Localidad'
        verbose_name_plural = ' Localidades'
        ordering = ['nombre']

    #Métodos
    def __str__(self):
        return "{}".format(self.nombre)

class Barrio(models.Model):

    #Choices
    ZONAS = ( (0, 'Urbana'),(1, 'Rural') )

    localidad = models.ForeignKey(Localidad,on_delete=models.PROTECT)
    nombre = models.CharField('Nombre',max_length=50,blank=False)
    zona = models.IntegerField('Zona',choices=ZONAS)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField('Activo',blank=True,default=True)

    #MetaData
    class Meta:
        db_table = 'barrio'
        verbose_name = 'Barrio'
        verbose_name_plural = 'Barrios'
        ordering = ['nombre']

    #Métodos
    def __str__(self):
        return "{}".format(self.nombre)