# Generated by Django 4.2.5 on 2023-10-02 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transaccion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='precio',
            field=models.PositiveIntegerField(),
        ),
    ]
