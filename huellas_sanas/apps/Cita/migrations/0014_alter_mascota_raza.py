# Generated by Django 4.2.5 on 2023-09-30 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cita', '0013_alter_mascota_raza'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mascota',
            name='raza',
            field=models.CharField(max_length=50),
        ),
    ]
