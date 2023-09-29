from django.db import models # Importa el módulo de modelos de Django
from django.contrib.auth.models import User # Importa el modelo de usuario incorporado de Django
from django.db.models.signals import post_delete # Importa la señal post_delete para detectar cambios en los modelos
from django.dispatch import receiver # Importa el decorador receiver para manejar señales


# Clase para almacenar información de los clientes
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con el modelo User de Django
    rut = models.CharField(max_length=12, default='')  # Campo para el RUT del cliente
    second_last_name = models.CharField(max_length=150, default='')  # Segundo apellido del cliente
    fecha_nacimiento = models.DateField()  # Fecha de nacimiento del cliente
    numero_telefono = models.CharField(max_length=15, default='')  # Número de teléfono del cliente
    
    def __str__(self):
        return self.user.username  # Para mostrar el nombre de usuario en la representación de cadena

# Clase para almacenar información de los empleados
class Empleado(models.Model):
    ROLE_CHOICES = [
        ('Recepcionista', 'Recepcionista'),
        ('Administrador', 'Administrador'),
        ('Veterinario', 'Veterinario'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con el modelo User de Django
    rut = models.CharField(max_length=12, default='')  # Campo para el RUT del empleado
    second_last_name = models.CharField(max_length=150, default='')  # Segundo apellido del empleado
    fecha_nacimiento = models.DateField()  # Fecha de nacimiento del empleado 
    numero_telefono = models.CharField(max_length=15, default='')  # Número de teléfono del empleado
    rol = models.CharField(max_length=50, choices=ROLE_CHOICES)  # Campo para el rol del empleado
    
    def __str__(self):
        return self.user.username  # Para mostrar el nombre de usuario en la representación de cadena

# Conecta la señal post_delete al modelo Cliente
@receiver(post_delete, sender=Cliente)
def eliminar_usuario_cliente(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()

# Conecta la señal post_delete al modelo Empleado
@receiver(post_delete, sender=Empleado)
def eliminar_usuario_empleado(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
