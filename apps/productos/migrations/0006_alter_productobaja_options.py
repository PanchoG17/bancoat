# Generated by Django 4.0.4 on 2023-02-14 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0005_alter_productobaja_options_alter_productobaja_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productobaja',
            options={'ordering': ['id'], 'verbose_name': 'Producto baja', 'verbose_name_plural': 'Productos baja'},
        ),
    ]
