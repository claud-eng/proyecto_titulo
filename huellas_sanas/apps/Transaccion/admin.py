from django.contrib import admin
from .models import Producto, Servicio, Carrito, OrdenDeCompra, DetalleOrden, OrdenDeVenta, DetalleOrdenVenta

# Register your models here.

admin.site.register(Producto)
admin.site.register(Servicio)
admin.site.register(Carrito)
admin.site.register(OrdenDeCompra)
admin.site.register(DetalleOrden)
admin.site.register(OrdenDeVenta)
admin.site.register(DetalleOrdenVenta)