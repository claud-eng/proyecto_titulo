from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.Usuario.models import Cliente  # Importa la clase Cliente

# Create your models here.

# Clase para registrar consultas y preguntas realizadas por los clientes
class Consulta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relación con el cliente que hizo la consulta
    asunto = models.CharField(max_length=100)
    mensaje = models.TextField()
    fecha_consulta = models.DateTimeField(auto_now_add=True)  # Fecha y hora de la consulta
    respondida = models.BooleanField(default=False)  # Marca si la consulta ha sido respondida

    def __str__(self):
        return f'Consulta de {self.cliente.user.username} el {self.fecha_consulta}'

