# Generated by Django 4.2.5 on 2023-09-25 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0009_alter_empleado_fecha_nacimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='rut',
            field=models.CharField(default='', max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='fecha_nacimiento',
            field=models.DateField(default='1'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='rut',
            field=models.CharField(default='', max_length=12, unique=True),
        ),
    ]
