# Generated by Django 4.0.1 on 2022-10-21 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('electrodependientes', '0009_alter_electrodependiente_archivo_formulario'),
    ]

    operations = [
        migrations.AddField(
            model_name='titulardesuministro',
            name='activo',
            field=models.BooleanField(default=True, editable=False, verbose_name='Activo'),
        ),
        migrations.AddField(
            model_name='titulardesuministro',
            name='fecha_baja',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='titulardesuministro',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='titulardesuministro',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='titulardesuministro',
            name='usuario_baja',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='titulardesuministro',
            name='usuario_creador',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='titulardesuministro',
            name='usuario_modificacion',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
    ]