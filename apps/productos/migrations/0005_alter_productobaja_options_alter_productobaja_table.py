# Generated by Django 4.0.4 on 2023-02-14 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0004_productobaja'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productobaja',
            options={'ordering': ['id'], 'verbose_name': 'Producto baja', 'verbose_name_plural': 'Productos_bajas'},
        ),
        migrations.AlterModelTable(
            name='productobaja',
            table='productos_bajas',
        ),
    ]
