from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from apps.abstract import General, Base, Contacto, Ubicacion, UbicacionDetallada
from apps.localizacion.models import Localidad, Pais, Provincia

class Empresa(General, Ubicacion):

    TIPOSERVICIO = (
        ('ELE', 'Eléctrica'),
        ('TEL', 'Telefónica'),
        ('SAN', 'Sanitaria'),
        ('GAS', 'Gas'),
        ('PRV', 'Proveedor')
    )

    pais = models.ForeignKey(Pais,verbose_name='Pais',on_delete=models.CASCADE, blank=False, null=False)
    provincia = ChainedForeignKey(Provincia,chained_field='pais',chained_model_field='pais', blank=True, null=True)
    localidad = ChainedForeignKey(Localidad,chained_field='provincia',chained_model_field='provincia', blank=True, null=True)

    razon_social = models.CharField(verbose_name='Razón Social', max_length=100, blank=True, null=True)
    cuit = models.CharField(verbose_name='C.U.I.T', max_length=11, blank=False, null=False)
    ingresos_brutos = models.CharField(verbose_name='Ingresos Brutos', max_length=11, blank=True, null=True)
    tipo_servicio =  models.CharField(verbose_name='Tipo de servicio', choices=TIPOSERVICIO, max_length=3)
    sitio_web = models.CharField(verbose_name='Sitio web', max_length=150, blank=True, null=True)

    codigo_area_c = models.CharField(verbose_name='Cód. de área celular', max_length=5, blank=True, null=True)
    numero_telefono_c = models.CharField(verbose_name='Nro. de celular', max_length=7, blank=True, null=True)
    codigo_area_f = models.CharField(verbose_name='Cód. de área teléfono fijo', max_length=5, blank=True, null=True)
    numero_telefono_f = models.CharField(verbose_name='Nro. de teléfono fijo', max_length=7, blank=True, null=True)
    email = models.EmailField(verbose_name='E-mail de contacto', blank=True, null=True)

    class Meta:
        db_table = 'empresa'
        verbose_name = 'Empresa'
        verbose_name_plural = '  Empresas'
        ordering = ['id']

    def __str__(self):
        return "{}".format(super().titulo)

class Sucursal(General, Ubicacion, Contacto):

    is_central = models.BooleanField(verbose_name='¿Es casa central?', choices=((False,'NO'),(True,'SI')), default=False,blank=False, null=False)

    class Meta:
        db_table = 'sucursal'
        verbose_name = 'Sucursal'
        verbose_name_plural = '  Sucursales'
        ordering = ['id']

    def __str__(self):
        return "{}".format(super().titulo)

class PuntoVenta(General):

    titulo= models.CharField(max_length= 30, verbose_name= 'Titulo', unique=False)
    codigo = models.CharField(unique=True, max_length=10)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    descripcion = None

    class Meta:
        db_table = 'puntos_venta'
        verbose_name = 'Punto de prestamo'
        verbose_name_plural = ' Puntos de prestamo'
        ordering = ['id']

    def __str__(self):
        return "{} - {}".format(self.sucursal, self.titulo)

class EstadoCivil(General):

    descripcion = None

    class Meta:
        db_table = 'estado_civil'
        verbose_name = 'Estado Civíl'
        verbose_name_plural = 'Estados Civíles'
        ordering = ['id']

    def __str__(self):
        return "{}".format(super().titulo)

class ObraSocial(General):

    descripcion = None

    class Meta:
        db_table = 'obra_social'
        verbose_name = 'Obra social'
        verbose_name_plural = 'Obras sociales'
        ordering = ['id']

    def __str__(self):
        return "{}".format(super().titulo)

class Genero(General):

    descripcion = None

    class Meta:
        db_table = 'genero'
        verbose_name = 'Genero'
        verbose_name_plural = 'Generos'
        ordering = ['id']

    def __str__(self):
        return "{}".format(super().titulo)


class TipoBaja(General):

    descripcion = None

    class Meta:
        db_table = 'tipo_baja'
        verbose_name = 'Motivo de baja'
        verbose_name_plural = 'Motivos de baja'
        ordering = ['id']

    def __str__(self):
        return "{}".format(super().titulo)

class TipoVivienda(General):

    descripcion = None

    class Meta:
        db_table = 'tipo_vivienda'
        verbose_name = 'Tipo de vivienda'
        verbose_name_plural = 'Tipos de Vivienda'
        ordering = ['id']

    def __str__(self):
        return "{}".format(super().titulo)


class TipoDiscapacidad(General):

    class Meta:
        db_table = 'tipo_discapacidad'
        verbose_name = 'Tipo de Discapacidad'
        verbose_name_plural = 'Tipos de Discapacidad'
        ordering = ['id']

    def __str__(self):
        return "{}".format(super().titulo)

class TipoDocumento(General):

    class Meta:
        db_table = 'tipo_documento'
        verbose_name = 'Tipo de Documentacion'
        verbose_name_plural = 'Tipos de Documentacion'
        ordering = ['id']

    def __str__(self):
        return "{}".format(super().titulo)

class TipoParentesco(Base):

    titulo= models.CharField(max_length= 20, verbose_name= 'Titulo')

    class Meta:
        db_table = 'tipo_parentesco'
        verbose_name = 'Tipo de Parentesco'
        verbose_name_plural = 'Tipos de Parentesco'
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.titulo)

class TipoComprobante(models.Model):
    codigo = models.CharField(unique=True, max_length=10)
    descripcion = models.CharField(max_length=25)
    incrementa = models.BooleanField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format( self.descripcion )

    class Meta:
        db_table = 'comprobante_tipo'
        verbose_name = 'Tipo de comprobante'
        verbose_name_plural = 'Tipos de Comprobante'
        ordering = ['codigo']


