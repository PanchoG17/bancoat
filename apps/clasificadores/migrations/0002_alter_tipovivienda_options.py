# Generated by Django 3.2.1 on 2022-09-28 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clasificadores', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tipovivienda',
            options={'ordering': ['id'], 'verbose_name': 'Tipo de vivienda', 'verbose_name_plural': 'Tipos de Vivienda'},
        ),
    ]
