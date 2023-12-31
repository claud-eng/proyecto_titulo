from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.Usuario.models import Cliente, Empleado  # Importa las clases Cliente y Empleado

# Create your models here.

# Clase para almacenar información sobre las mascotas de los clientes
class Mascota(models.Model):
    ESPECIES_CHOICES = (
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
    )
    ESTADO_MASCOTA_CHOICES = [
    ('Sin atender', 'Sin atender'),
    ('En guardería', 'En guardería'),
    ('Siendo atendida', 'Siendo atendida'),
    ('En cirugía', 'En cirugía'),
    ('En cuidado post atención', 'En cuidado post atención'),
    ('Dada de alta', 'Dada de alta'),
    ('Fallecida', 'Fallecida'),
    # Agrega más opciones según sea necesario
]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50, choices=ESPECIES_CHOICES)
    raza = models.CharField(max_length=50)  
    estado = models.CharField(max_length=50, choices=ESTADO_MASCOTA_CHOICES, default='Sin atender', blank=True)

    def __str__(self):
        return self.nombre
    
class Cita(models.Model):
    MOTIVO_CHOICES = (
        ('Consulta Médica General', 'Consulta Médica General'),
        ('Esterilización', 'Esterilización'),
        ('Guardería', 'Guardería'),
        ('Peluquería', 'Peluquería'),
        ('Vacunación', 'Vacunación'),
    )

    ESTADO_CHOICES = (
        ('Programada', 'Programada'),
        ('Cancelada', 'Cancelada'),
        ('Realizada', 'Realizada'),
    )

    fecha = models.DateField()
    hora = models.TimeField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    veterinario = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'Veterinario'}  # Filtra por el rol 'Veterinario'
    )
    motivo = models.CharField(max_length=50, choices=MOTIVO_CHOICES)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Programada')  # Establece el valor por defecto
    ha_pagado = models.BooleanField(default=False, verbose_name="¿Ha pagado?")
    
    def __str__(self):
        return f'Cita para el cliente {self.cliente.user.username} con {self.veterinario.user.username} el {self.fecha} a las {self.hora}'
