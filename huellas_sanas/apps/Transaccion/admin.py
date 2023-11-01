from django.contrib import admin
from .models import Producto, Servicio, Carrito, OrdenDeCompra

# Register your models here.

admin.site.register(Producto)
admin.site.register(Servicio)
admin.site.register(Carrito)
admin.site.register(OrdenDeCompra)