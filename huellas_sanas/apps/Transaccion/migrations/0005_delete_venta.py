# Generated by Django 4.2.5 on 2023-10-31 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Transaccion', '0004_producto_categoria'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Venta',
        ),
    ]