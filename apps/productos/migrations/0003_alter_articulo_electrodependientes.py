# Generated by Django 4.0.1 on 2022-10-03 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_alter_producto_numero_serie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='electrodependientes',
            field=models.BooleanField(choices=[(True, 'SI'), (False, 'NO')], default=False, verbose_name='Uso electrodependiente'),
        ),
    ]