# Generated by Django 4.2.5 on 2023-09-28 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cita', '0006_alter_mascota_raza'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='estado',
            field=models.CharField(choices=[('Programada', 'Programada'), ('Cancelada', 'Cancelada'), ('Realizada', 'Realizada')], max_length=50),
        ),
        migrations.AlterField(
            model_name='cita',
            name='motivo',
            field=models.CharField(choices=[('Consulta Médica General', 'Consulta Médica General'), ('Esterilización', 'Esterilización'), ('Guardería', 'Guardería'), ('Peluquería', 'Peluquería'), ('Vacunación', 'Vacunación')], max_length=50),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='especie',
            field=models.CharField(choices=[('Perro', 'Perro'), ('Gato', 'Gato')], max_length=50),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='raza',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]