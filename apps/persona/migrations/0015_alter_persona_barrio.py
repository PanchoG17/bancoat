# Generated by Django 4.0.4 on 2023-02-13 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0014_alter_persona_barrio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='barrio',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Barrio'),
        ),
    ]