# Generated by Django 4.2.5 on 2023-09-29 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0011_alter_cliente_rut_alter_empleado_rut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha_nacimiento',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='fecha_nacimiento',
            field=models.DateField(),
        ),
    ]