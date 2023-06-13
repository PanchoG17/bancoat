from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from apps.productos.models import Producto, Articulo, Marca
from apps.persona.models import Beneficiario
from apps.clasificadores.models import Empresa, Sucursal, PuntoVenta, TipoComprobante
from apps.localizacion.models import Pais
from apps.electrodependientes.models import Electrodependiente

class Numerador(models.Model):
    numeracion = models.IntegerField()
    tipo_comprobante = models.ForeignKey(TipoComprobante, on_delete=models.CASCADE)
    punto_venta = models.ForeignKey(PuntoVenta, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comprobante_numerador'
        verbose_name = 'Numeración de comprobantes'
        verbose_name_plural = 'N° de comprobantes'
        ordering = ['tipo_comprobante']

    def __str__(self):
        return "{} - {} - {}".format( self.tipo_comprobante, self.punto_venta ,  str(self.numeracion).zfill(6) )

class Comprobante(models.Model):

    PROCEDENCIA = (
        ('Adquirido', 'Adquirido'),
        ('Donado', 'Donado'),
        ('Fondo propio', 'Fondo propio')
    )

    numero = models.CharField(max_length=25, blank=True, null=True, editable=False)
    tipo_comprobante = models.ForeignKey(TipoComprobante, on_delete=models.CASCADE, blank=False, null=False)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    fecha_operacion = models.DateTimeField(verbose_name='Fecha de operación', default=datetime.now, blank=False, null=False)
    punto_venta = models.ForeignKey(PuntoVenta, on_delete=models.CASCADE, verbose_name='Punto de préstamo', blank=False, null=False)
    procedencia = models.CharField( verbose_name='Procedencia', max_length=20, choices=PROCEDENCIA, blank=True, null=True )
    proveedor = models.ForeignKey(Empresa, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Proveedor')
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    usuario_creador= models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comprobante'
        verbose_name = 'Comprobante'
        verbose_name_plural = 'Comprobantes'
        ordering = ['id']

    def __str__(self):
        return self.numero

    def save(self):

        try:
            # Aumento el numerador
            numerador = Numerador.objects.get(tipo_comprobante = self.tipo_comprobante, punto_venta = self.punto_venta)
            numerador.numeracion += 1
            numerador.save()

        except Numerador.DoesNotExist:
            # Si no existe un numerador de comprobante se crea uno nuevo
            numerador = Numerador(
                numeracion=1,
                punto_venta = self.punto_venta,
                tipo_comprobante = self.tipo_comprobante
            )
            numerador.save()

        # El N° de comprobante se setea según el punto de venta y tipo de comprobante + Numerador, eg: 'CE USH 01-000001'
        self.numero = f"{self.tipo_comprobante.codigo} {self.punto_venta.codigo}-{str(numerador.numeracion).zfill(6)}"
        super(Comprobante, self).save()

class DetalleEntrada(models.Model):

    modelo_producto = []
    for y in range(2000, (datetime.now().year + 1)):
        modelo_producto.append((y, y))

    ESTADO = (
        ('Nuevo', 'Nuevo'),
        ('Usado', 'Usado'),
        ('Reacondicionado', 'Reacondicionado')
    )

    comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE,verbose_name='Nro. de Comprobante')
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, blank=False, null=False)
    marca = models.ForeignKey( Marca, on_delete=models.CASCADE )
    modelo = models.IntegerField( choices=modelo_producto, default=datetime.now().year )
    numero_serie = models.CharField( verbose_name='N° Serie', max_length=15, blank=True, null=True, unique=True )
    pais_origen = models.ForeignKey( Pais, verbose_name='Origen', on_delete=models.CASCADE )
    estado = models.CharField( verbose_name='Estado', max_length=20, choices=ESTADO, blank=False, null=False )
    valor = models.PositiveIntegerField( verbose_name='Valor', blank=False,null=False )

    class Meta:
        db_table = 'comprobante_entradas'
        verbose_name = 'Detalle de Comprobante'
        verbose_name_plural = 'Detalle de Comprobantes'
        ordering = ['id']

    def __str__(self):
        return "{}".format( self.comprobante )

    def save(self):

        try:
            # Productos
            producto = Producto(
                articulo=self.articulo,
                marca=self.marca,
                modelo=self.modelo,
                numero_serie=self.numero_serie,
                origen=self.pais_origen,
                estado=self.estado,
                valor=self.valor,
                situacion='DISP',
                sucursal=self.comprobante.sucursal
            )
            producto.save()

            # Kardex
            kardex = Kardex(
                articulo = self.articulo,
                comprobante= self.comprobante,
                fecha_operacion= self.comprobante.fecha_operacion,
                sucursal= self.comprobante.sucursal,
                cantidad_ingreso = 1,
                cantidad_salida = 0
            )
            kardex_anterior = Kardex.objects.filter(articulo = producto.articulo, sucursal = self.comprobante.sucursal).last()

            # Si no existe un kardex anterior seteo la cantidad total = 1
            kardex.cantidad_total = 1 if not kardex_anterior else kardex_anterior.cantidad_total + 1
        except:
            pass

        super(DetalleEntrada, self).save()
        kardex.save()

class DetallePrestamo(models.Model):
    comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE,verbose_name='Nro. de Comprobante', editable=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=False, null=False)

    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Beneficiario')
    electro = models.ForeignKey(Electrodependiente, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Electrodependiente')

    fecha_otorgamiento = models.DateField(verbose_name='Fecha de otorgamiento', blank=False, null=False, default=datetime.now)
    fecha_devolucion = models.DateField(verbose_name='Fecha de devolución', blank=False, null=False, default=None)

    regresado = models.BooleanField(default=False, editable=False)
    baja = models.BooleanField(default=False, editable=False)

    class Meta:
        db_table = 'comprobante_prestamo'
        verbose_name = 'Detalle comprobante de prestamo'
        verbose_name_plural = 'Detalle comprobantes de prestamo'
        ordering = ['id']

    def __str__(self):
        return "{}".format( self.comprobante )

    def save(self):
        try:
            # Producto
            producto = Producto.objects.get(id = self.producto.pk)
            producto.situacion = 'OTO'
            producto.save()

            # Kardex
            kardex_anterior = Kardex.objects.filter(articulo = producto.articulo,sucursal = self.comprobante.sucursal).last()
            kardex = Kardex(
                articulo = producto.articulo,
                comprobante= self.comprobante,
                fecha_operacion= self.comprobante.fecha_operacion,
                sucursal= self.comprobante.sucursal,
                cantidad_ingreso = 0,
                cantidad_salida = 1,
                cantidad_total = kardex_anterior.cantidad_total - 1
            )

        except:
            pass

        super(DetallePrestamo, self).save()
        kardex.save()

class DetalleDevolucion(models.Model):
    comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE,verbose_name='Nro. de Comprobante', editable=False)
    comprobante_prestamo = models.OneToOneField(DetallePrestamo, on_delete=models.CASCADE, verbose_name='Comprobante de prestamo', blank=True, null=True, editable=False)
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE, editable=False, blank=True, null=True)
    electro = models.ForeignKey(Electrodependiente, on_delete=models.CASCADE, editable=False, blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    fecha_devolucion = models.DateField(verbose_name='Fecha de devolución', blank=False, null=False, default=datetime.now)

    class Meta:
        db_table = 'comprobante_devolucion'
        verbose_name = 'Detalle comprobante de devolución'
        verbose_name_plural = 'Detalle comprobantes de devolución'
        ordering = ['id']

    def __str__(self):
        return "{}".format( self.producto )

    def save(self):

        try:
            # Producto
            producto = Producto.objects.get(id = self.producto.pk)
            producto.situacion = 'DISP'
            producto.save()

            # Prestamo
            prestamo = DetallePrestamo.objects.filter(producto = self.producto.pk, regresado = False)

            # Devolucion - Verifica si el prestamo corresponde a electro o beneficiario -
            self.comprobante_prestamo = prestamo.last()

            if not prestamo.last().beneficiario:
                self.electro = prestamo.last().electro
            else:
                self.beneficiario = prestamo.last().beneficiario

            prestamo = prestamo.update(regresado = True)

            # Kardex
            kardex_anterior = Kardex.objects.filter( articulo = producto.articulo, sucursal = self.comprobante.sucursal).last()
            kardex = Kardex(
                articulo = producto.articulo,
                comprobante= self.comprobante,
                fecha_operacion= self.comprobante.fecha_operacion,
                sucursal= self.comprobante.sucursal,
                cantidad_ingreso = 1,
                cantidad_salida = 0,
                cantidad_total = kardex_anterior.cantidad_total + 1
            )

        except Exception as e:
            pass

        super(DetalleDevolucion, self).save()
        kardex.save()

class DetalleRenovacion(models.Model):
    comprobante = models.OneToOneField(Comprobante, on_delete=models.CASCADE,verbose_name='Nro. de Comprobante', editable=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Beneficiario')
    electro = models.ForeignKey(Electrodependiente, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Electrodependiente')
    anterior_vencimiento = models.DateField(verbose_name='Vencimiento anterior', blank=False, null=False, default=None)
    nuevo_vencimiento = models.DateField(verbose_name='Nuevo vencimiento', blank=False, null=False, default=None)

    class Meta:
        db_table = 'comprobante_renovacion'
        verbose_name = 'Detalle comprobante de renovación'
        verbose_name_plural = 'Detalle comprobantes de renovación'
        ordering = ['id']

    def __str__(self):
        return "{}".format( self.comprobante )

    def save(self):
        try:
            # Producto
            producto = Producto.objects.get(id = self.producto.pk)

            # Prestamo
            prestamo = DetallePrestamo.objects.filter(producto = self.producto.pk, regresado = False)
            prestamo.update(fecha_devolucion = self.nuevo_vencimiento)

            # Kardex
            kardex_anterior = Kardex.objects.filter(articulo = producto.articulo, sucursal = self.comprobante.sucursal).last()
            kardex = Kardex(
                articulo = producto.articulo,
                comprobante= self.comprobante,
                fecha_operacion= self.comprobante.fecha_operacion,
                sucursal= self.comprobante.sucursal,
                cantidad_ingreso = 0,
                cantidad_salida = 0,
                cantidad_total = kardex_anterior.cantidad_total
            )

        except:
            pass

        super(DetalleRenovacion, self).save()
        kardex.save()

class Kardex(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE, verbose_name='Nro. de comprobante')
    fecha_operacion = models.DateTimeField(verbose_name='Fecha de operación', default=datetime.now, blank=False, null=False)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, verbose_name='Sucursal')

    cantidad_ingreso = models.IntegerField()
    cantidad_salida = models.IntegerField()
    cantidad_total = models.IntegerField()

    class Meta:
        db_table = 'kardex'
        verbose_name = 'Kardex'
        verbose_name_plural = 'Kardex'
        ordering = ['id']

    def __str__(self):
        return "{}".format( self.comprobante )