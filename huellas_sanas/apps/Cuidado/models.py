from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.Usuario.models import Cliente, Empleado  # Importa las clases Cliente y Empleado
from apps.Cita.models import Mascota # Importa la clase Mascota

# Create your models here.

# Clase para registrar fichas médicas y tratamientos para las mascotas
class Ficha(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)  # Relación con la mascota asociada a la ficha
    veterinario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el veterinario que crea la ficha
    fecha = models.DateField()
    medicamento = models.CharField(max_length=100)
    dosis = models.CharField(max_length=50)
    instrucciones = models.TextField()

    def __str__(self):
        return f'Ficha para {self.mascota.nombre} por {self.veterinario.username} el {self.fecha}'
    