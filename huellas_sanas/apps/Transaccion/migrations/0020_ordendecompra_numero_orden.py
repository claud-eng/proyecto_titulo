# Generated by Django 4.2.5 on 2023-11-14 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transaccion', '0019_ordendecompra_monto_cuotas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordendecompra',
            name='numero_orden',
            field=models.CharField(blank=True, max_length=26, null=True),
        ),
    ]
