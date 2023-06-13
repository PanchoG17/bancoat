# Generated by Django 3.2.1 on 2022-09-21 03:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clasificadores', '0001_initial'),
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Electrodependiente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, null=True)),
                ('fecha_baja', models.DateTimeField(blank=True, editable=False, null=True)),
                ('activo', models.BooleanField(default=True, editable=False, verbose_name='Activo')),
                ('usuario_modificacion', models.IntegerField(blank=True, editable=False, null=True)),
                ('usuario_baja', models.IntegerField(blank=True, editable=False, null=True)),
                ('us', models.BooleanField(choices=[(True, 'SI'), (False, 'NO')], verbose_name='U.S')),
                ('rupe', models.BooleanField(choices=[(True, 'SI'), (False, 'NO')], verbose_name='RUPE')),
                ('pension_nacional', models.BooleanField(choices=[(True, 'SI'), (False, 'NO')], verbose_name='Pensión Nacional')),
                ('cud', models.BooleanField(choices=[(True, 'SI'), (False, 'NO')], verbose_name='CUD')),
                ('fecha_vencimiento_cud', models.DateField(blank=True, null=True, verbose_name='Fecha de vencimiento CUD')),
                ('persona_electrodependiente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='persona.persona', verbose_name='Persona')),
                ('usuario_creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Persona Electrodependiente',
                'verbose_name_plural': ' Electrodependientes',
                'db_table': 'electrodependiente',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TitularDeSuministro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_cliente', models.CharField(max_length=20, verbose_name='Número de cliente')),
                ('electrodependiente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='electrodependientes.electrodependiente', verbose_name='Electrodependiente')),
                ('proveedor_suministro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clasificadores.empresa', verbose_name='Compañía proveedora del suministro')),
                ('titular_servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persona.persona', verbose_name='Titular del servicio eléctrico')),
                ('vinculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clasificadores.tipoparentesco', verbose_name='Vinculo con la persona solicitante')),
            ],
            options={
                'verbose_name': 'Titular de suministro',
                'verbose_name_plural': 'Titulares de suministros',
                'db_table': 'titular_de_suministro',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, null=True)),
                ('fecha_baja', models.DateTimeField(blank=True, editable=False, null=True)),
                ('activo', models.BooleanField(default=True, editable=False, verbose_name='Activo')),
                ('usuario_modificacion', models.IntegerField(blank=True, editable=False, null=True)),
                ('usuario_baja', models.IntegerField(blank=True, editable=False, null=True)),
                ('matricula_profesional', models.CharField(max_length=10, verbose_name='Matrícula profesional')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persona.persona', verbose_name='Persona')),
                ('usuario_creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Médico',
                'verbose_name_plural': ' Médicos',
                'db_table': 'medico',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Diagnostico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, null=True)),
                ('fecha_baja', models.DateTimeField(blank=True, editable=False, null=True)),
                ('activo', models.BooleanField(default=True, editable=False, verbose_name='Activo')),
                ('historia_clinica', models.TextField(blank=True, null=True, verbose_name='Resumen datallado de la historia clínica')),
                ('diagnostico', models.TextField(blank=True, null=True, verbose_name='Diagnóstico CIE10')),
                ('equipo_dialisis', models.BooleanField(choices=[(True, 'SI'), (False, 'NO')], default=False, verbose_name='Diálisis peritoneal automatizada (DPA) domiciliaria')),
                ('equipo_alimentacion', models.BooleanField(choices=[(True, 'SI'), (False, 'NO')], default=False, verbose_name='Bomba de infusión contínua, bomba de alimentación enteral o parenteral')),
                ('equipo_ventilacion', models.TextField(blank=True, null=True, verbose_name='Equipos relacionados al soporte de la ventilación')),
                ('otro', models.TextField(blank=True, null=True, verbose_name='Otros')),
                ('tiempo_requerido', models.CharField(choices=[('6', 'Hasta 6 meses'), ('1', 'Hasta 1 año'), ('2', 'Hasta 2 años')], max_length=1, verbose_name='Tiempo estimado de requerimiento')),
                ('fecha_diagnostico', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha de diagnóstico')),
                ('electrodependiente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='electrodependientes.electrodependiente', verbose_name='Electrodependiente')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='electrodependientes.medico')),
            ],
            options={
                'verbose_name': 'Diagnóstico',
                'verbose_name_plural': 'Diagnósticos',
                'db_table': 'diagnostico',
                'ordering': ['id'],
            },
        ),
    ]
