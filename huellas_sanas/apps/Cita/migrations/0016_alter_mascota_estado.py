# Generated by Django 4.2.5 on 2023-09-30 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cita', '0015_mascota_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mascota',
            name='estado',
            field=models.CharField(choices=[('ConSuDueño', 'Con su dueño'), ('EnGuarderia', 'En Guardería'), ('SiendoAtendida', 'Siendo atendida'), ('EnCirugia', 'En cirugía'), ('EnCuidado', 'En cuidado post atención'), ('DadaDeAlta', 'Data de alta'), ('Fallecida', 'Fallecida')], default='Con Su Dueño', max_length=50),
        ),
    ]