# Generated by Django 4.2.5 on 2023-09-28 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cita', '0002_rename_mascota_cita_mascota'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mascota',
            name='historial_medico',
        ),
    ]