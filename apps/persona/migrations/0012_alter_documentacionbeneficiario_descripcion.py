# Generated by Django 4.0.1 on 2022-12-13 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0011_remove_documentacionbeneficiario_fecha_vencimiento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentacionbeneficiario',
            name='descripcion',
            field=models.CharField(max_length=80, verbose_name='Descripción'),
        ),
    ]