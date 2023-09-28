# Generated by Django 4.2.5 on 2023-09-28 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0011_alter_cliente_rut_alter_empleado_rut'),
        ('Cita', '0007_alter_cita_estado_alter_cita_motivo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='veterinario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuario.empleado'),
        ),
    ]