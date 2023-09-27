from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.Usuario.models import Cliente, Empleado  # Importa las clases Cliente y Empleado

# Create your models here.

# Clase para almacenar información sobre las mascotas de los clientes
class Mascota(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relación con el cliente propietario de la mascota
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=50)
    historial_medico = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Cita(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    veterinario = models.ForeignKey(Empleado, on_delete=models.CASCADE, limit_choices_to={'user__is_staff': True})
    motivo = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)  # Por ejemplo, 'Programada', 'Cancelada', 'Realizada'

    def __str__(self):
        return f'Cita para {self.cliente.user.username} con {self.veterinario.user.username} el {self.fecha} a las {self.hora}'
