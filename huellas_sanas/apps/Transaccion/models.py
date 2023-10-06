from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.Usuario.models import Cliente, Empleado  # Importa las clases Cliente y Empleado

# Create your models here.

# Clase para almacenar información de productos
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField() 
    cantidad_stock = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

# Clase para almacenar información de servicios
class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField() 

    def __str__(self):
        return self.nombre

# Clase para registrar los productos o servicios en el carrito de un cliente
class Carrito(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.cliente.username} - {self.item.nombre}'

class Venta(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Venta de {self.cliente.username} - Total: {self.total}'


