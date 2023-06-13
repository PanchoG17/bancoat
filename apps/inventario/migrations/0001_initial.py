# Generated by Django 4.0.1 on 2023-05-15 13:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0006_alter_productobaja_options'),
        ('persona', '0016_alter_persona_cuit_alter_persona_email_and_more'),
        ('clasificadores', '0008_alter_empresa_codigo_area_c_alter_empresa_email_and_more'),
        ('electrodependientes', '0016_merge_20230208_1112'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('localizacion', '0002_alter_pais_codigo_alfa2_alter_pais_codigo_alfa3_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comprobante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(blank=True, editable=False, max_length=25, null=True)),
                ('fecha_operacion', models.DateTimeField(default=datetime.datetime.now, verbose_name='Fecha de operación')),
                ('procedencia', models.CharField(blank=True, choices=[('Adquirido', 'Adquirido'), ('Donado', 'Donado'), ('Fondo propio', 'Fondo propio')], max_length=20, null=True, verbose_name='Procedencia')),
                ('descripcion', models.CharField(blank=True, max_length=25, null=True)),
                ('proveedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clasificadores.empresa', verbose_name='Proveedor')),
                ('punto_venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clasificadores.puntoventa', verbose_name='Punto de préstamo')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clasificadores.sucursal')),
                ('tipo_comprobante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clasificadores.tipocomprobante')),
                ('usuario_creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comprobante',
                'verbose_name_plural': 'Comprobantes',
                'db_table': 'comprobante',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='RenovacionesPrestamos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anterior_vencimiento', models.DateField(default=None, verbose_name='Vencimiento anterior')),
                ('nuevo_vencimiento', models.DateField(default=None, verbose_name='Nuevo vencimiento')),
                ('beneficiario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='persona.beneficiario', verbose_name='Beneficiario')),
                ('comprobante', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='inventario.comprobante', verbose_name='Nro. de Comprobante')),
                ('electro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='electrodependientes.electrodependiente', verbose_name='Electrodependiente')),
                ('usuario_creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Renovacion de préstamo',
                'verbose_name_plural': 'Renovaciones de préstamos',
                'db_table': 'prestamos_renovaciones',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Numerador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeracion', models.IntegerField()),
                ('punto_venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clasificadores.puntoventa')),
                ('tipo_comprobante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clasificadores.tipocomprobante')),
            ],
            options={
                'verbose_name': 'Numeración de comprobantes',
                'verbose_name_plural': 'N° de comprobantes',
                'db_table': 'comprobante_numerador',
                'ordering': ['tipo_comprobante'],
            },
        ),
        migrations.CreateModel(
            name='Kardex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_operacion', models.DateTimeField(default=datetime.datetime.now, verbose_name='Fecha de operación')),
                ('cantidad_ingreso', models.IntegerField()),
                ('cantidad_salida', models.IntegerField()),
                ('cantidad_total', models.IntegerField()),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.articulo')),
                ('comprobante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.comprobante', verbose_name='Nro. de comprobante')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clasificadores.sucursal', verbose_name='Sucursal')),
            ],
            options={
                'verbose_name': 'Kardex',
                'verbose_name_plural': 'Kardex',
                'db_table': 'kardex',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DetallePrestamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_otorgamiento', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de otorgamiento')),
                ('fecha_devolucion', models.DateField(default=None, verbose_name='Fecha de devolución')),
                ('regresado', models.BooleanField(default=False, editable=False)),
                ('baja', models.BooleanField(default=False, editable=False)),
                ('beneficiario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='persona.beneficiario', verbose_name='Beneficiario')),
                ('comprobante', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='inventario.comprobante', verbose_name='Nro. de Comprobante')),
                ('electro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='electrodependientes.electrodependiente', verbose_name='Electrodependiente')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
            ],
            options={
                'verbose_name': 'Detalle comprobante de prestamo',
                'verbose_name_plural': 'Detalle comprobantes de prestamo',
                'db_table': 'comprobante_prestamo',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DetalleEntrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.IntegerField(choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023)], default=2023)),
                ('numero_serie', models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='N° Serie')),
                ('estado', models.CharField(choices=[('Nuevo', 'Nuevo'), ('Usado', 'Usado'), ('Reacondicionado', 'Reacondicionado')], max_length=20, verbose_name='Estado')),
                ('valor', models.PositiveIntegerField(verbose_name='Valor')),
                ('cantidad', models.PositiveIntegerField(default=1, editable=False)),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.articulo')),
                ('comprobante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.comprobante', verbose_name='Nro. de Comprobante')),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.marca')),
                ('pais_origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localizacion.pais', verbose_name='Origen')),
            ],
            options={
                'verbose_name': 'Detalle de Comprobante',
                'verbose_name_plural': 'Detalle de Comprobantes',
                'db_table': 'comprobante_entradas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DetalleDevolucion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_devolucion', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de devolución')),
                ('comprobante', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='inventario.comprobante', verbose_name='Nro. de Comprobante')),
                ('comprobante_prestamo', models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.detalleprestamo', verbose_name='Comprobante de prestamo')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'Detalle comprobante de devolución',
                'verbose_name_plural': 'Detalle comprobantes de devolución',
                'db_table': 'comprobante_devolucion',
                'ordering': ['id'],
            },
        ),
    ]