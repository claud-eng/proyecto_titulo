from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.Transaccion.models import Producto, Servicio  # Importa las clases Producto y Servicio

# Create your models here.

# Clase para registrar datos utilizados en informes estadísticos automatizados
class Reporte(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, blank=True, null=True)
    tipo_servicio = models.CharField(max_length=100)  
    cantidad_pagada = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()

    # Campos adicionales para informes estadísticos
    cantidad_vendida = models.PositiveIntegerField()  # Cantidad de veces que se vendió el producto/servicio
    total_ingresos = models.DecimalField(max_digits=10, decimal_places=2)  # Total de ingresos por el producto/servicio

    def __str__(self):
        return f'Reporte de {self.tipo_servicio} el {self.fecha}'
