# Generated by Django 4.0.1 on 2022-10-03 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0006_rename_beneficiario_beneficiario_persona_beneficiaria_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentacionbeneficiario',
            name='beneficiario',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='persona.beneficiario', verbose_name='Beneficiario'),
        ),
    ]
