from django.urls import path, include  # Importa path para definir rutas de URL e include para incluir otras configuraciones de URL
from . import views  # Importa las vistas definidas en el directorio actual (directorio donde se encuentra este archivo)

urlpatterns = [
    # Ruta para gestionar el inventario siendo administrador
    path('gestionar_inventario', views.gestionar_inventario, name='gestionar_inventario'),
    # Rutas para los productos
    path('listar_productos', views.listar_productos, name="listar_productos"),
    path('agregar_producto', views.agregar_producto, name="agregar_producto"),
    path('editar_producto/<int:producto_id>', views.editar_producto, name="editar_producto"),
    path('borrar_producto/<int:producto_id>', views.borrar_producto, name="borrar_producto"),
    path('confirmar-borrar-producto/<int:producto_id>/', views.confirmar_borrar_producto, name='confirmar_borrar_producto'),

    # Rutas para los servicios
    path('listar_servicios', views.listar_servicios, name="listar_servicios"),
    path('agregar_servicio', views.agregar_servicio, name="agregar_servicio"),
    path('editar_servicio/<int:servicio_id>', views.editar_servicio, name="editar_servicio"),
    path('borrar_servicio/<int:servicio_id>', views.borrar_servicio, name="borrar_servicio"),
    path('confirmar-borrar-servicio/<int:servicio_id>/', views.confirmar_borrar_servicio, name='confirmar_borrar_servicio'),
]