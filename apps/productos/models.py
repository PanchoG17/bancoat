from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey

from apps.clasificadores.models import General, Sucursal
from apps.localizacion.models import Localidad, Pais

class Categoria(General):
    descripcion = None

    class Meta:
        db_table = 'producto_categoria'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

    def __str__(self):
        return "{}".format( super().titulo)

class Subcategoria(General):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = None

    class Meta:
        db_table = 'producto_subcategoria'
        verbose_name = 'Subcategoria'
        verbose_name_plural = 'Subcategorias'
        ordering = ['id']

    def __str__(self):
        return "{}".format( super().titulo )

class Marca(General):
    descripcion = None

    class Meta:
        db_table = 'producto_marca'
        verbose_name = 'Marca'
        verbose_name_plural = ' Marcas'
        ordering = ['id']

    def __str__(self):
        return "{}".format(super().titulo)

class Articulo(General):
    descripcion = None
    categoria = models.ForeignKey( Categoria, on_delete=models.CASCADE )
    subcategoria = ChainedForeignKey( Subcategoria, chained_field='categoria', chained_model_field='categoria', show_all=False, auto_choose=True, sort=True )
    electrodependientes = models.BooleanField( choices=((True,'SI'),(False,'NO')), default=False, verbose_name='Uso electrodependiente' )

    class Meta:
        db_table = 'articulo'
        verbose_name = 'Articulo'
        verbose_name_plural = ' Articulos'
        ordering = ['id']

    def __str__(self):
        return "{}".format(super().titulo.capitalize())

class Producto(models.Model):

    SITUACION = (
        ('DISP', 'Disponible'),
        ('OTO', 'Otorgado'),
        ('NO_DISP', 'No disponible')
    )

    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    marca = models.ForeignKey( Marca, on_delete=models.CASCADE )
    modelo = models.IntegerField()
    numero_serie = models.CharField( verbose_name='Numero de serie', max_length=15,unique=True, blank=False, null=False )
    origen = models.ForeignKey( Pais, verbose_name='País de origen', on_delete=models.CASCADE )
    estado = models.CharField( verbose_name='Estado de uso', max_length=20, blank=False, null=False )
    valor = models.DecimalField( verbose_name='Valor monetario', max_digits=10, decimal_places=2,blank=False,null=False )
    situacion = models.CharField( verbose_name='Situación del producto',choices=SITUACION, max_length=10, blank=False, null=False)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = '  Productos'
        ordering = ['id']

    def __str__(self):
        return "{} - {} - {}".format(self.articulo.titulo, self.marca, self.numero_serie )

class ProductoBaja(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, blank=False, null=False)
    motivo_baja= models.CharField(max_length=30, verbose_name= 'Motivo de baja', blank=False, null=False)
    fecha_baja = models.DateField(verbose_name='Fecha de baja', blank=False, null=False)
    usuario_baja= models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        db_table = 'productos_bajas'
        verbose_name = 'Producto baja'
        verbose_name_plural = 'Productos baja'
        ordering = ['id']

    def __str__(self):
        return self.producto