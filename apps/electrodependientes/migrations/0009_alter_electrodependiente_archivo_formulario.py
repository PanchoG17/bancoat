# Generated by Django 4.0.1 on 2022-10-20 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electrodependientes', '0008_electrodependiente_archivo_formulario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electrodependiente',
            name='archivo_formulario',
            field=models.ImageField(blank=True, null=True, upload_to='documentacion/electros/', verbose_name='Adjuntar Formulario físico'),
        ),
    ]