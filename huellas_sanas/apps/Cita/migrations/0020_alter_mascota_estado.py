# Generated by Django 4.2.5 on 2023-10-26 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cita', '0019_alter_mascota_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mascota',
            name='estado',
            field=models.CharField(blank=True, choices=[('Sin atender', 'Sin atender'), ('En guardería', 'En guardería'), ('Siendo atendida', 'Siendo atendida'), ('En cirugía', 'En cirugía'), ('En cuidado post atención', 'En cuidado post atención'), ('Dada de alta', 'Dada de alta'), ('Fallecida', 'Fallecida')], default='Sin atender', max_length=50),
        ),
    ]