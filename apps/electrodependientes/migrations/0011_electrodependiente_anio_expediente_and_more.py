# Generated by Django 4.0.4 on 2023-01-25 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electrodependientes', '0010_titulardesuministro_activo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='electrodependiente',
            name='anio_expediente',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Expte. año'),
        ),
        migrations.AddField(
            model_name='electrodependiente',
            name='letra_expediente',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Expte. letra'),
        ),
        migrations.AddField(
            model_name='electrodependiente',
            name='nro_expediente',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Expte. número'),
        ),
    ]
