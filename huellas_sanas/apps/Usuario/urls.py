from django.urls import path, include  # Importa path para definir rutas de URL e include para incluir otras configuraciones de URL
from . import views  # Importa las vistas definidas en el directorio actual (directorio donde se encuentra este archivo)

urlpatterns = [ 
    # Ruta para actualizar los datos personales como cliente excluyendo la contraseña
    path('actualizar_datos_personales_cliente', views.actualizar_datos_personales_cliente, name='actualizar_datos_personales_cliente'),
    # Ruta para cambiar la contraseña
    path('cambiar_contraseña_cliente', views.cambiar_contraseña_cliente, name='cambiar_contraseña_cliente'),
    # Ruta para gestionar las cuentas siendo administrador
    path('gestionar_cuentas', views.gestionar_cuentas, name='gestionar_cuentas'),
    # Rutas para clientes
    # Listar los clientes de la bd
    path('listar_clientes', views.listar_clientes, name="listar_clientes"),
    # Agregar un cliente
    path('agregar_cliente', views.agregar_cliente, name="agregar_cliente"),
    # Editar un cliente
    path('editar_cliente/<int:cliente_id>', views.editar_cliente, name="editar_cliente"),
    # Borrar un cliente
    path('borrar_cliente/<int:cliente_id>', views.borrar_cliente, name="borrar_cliente"),
    # Confirmar antes de borrar un cliente
    path('confirmar-borrar-cliente/<int:cliente_id>/', views.confirmar_borrar_cliente, name='confirmar_borrar_cliente'),
    # Rutas para empleados
    # Listar los empleados de la bd
    path('listar_empleados', views.listar_empleados, name="listar_empleados"),
    # Agregar un empleado
    path('agregar_empleado', views.agregar_empleado, name="agregar_empleado"),
    # Editar un empleado
    path('editar_empleado/<int:empleado_id>', views.editar_empleado, name="editar_empleado"),
    # Borrar un empleado
    path('borrar_empleado/<int:empleado_id>', views.borrar_empleado, name="borrar_empleado"),
    # Confirmar antes de borrar un empleado
    path('confirmar-borrar-empleado/<int:empleado_id>/', views.confirmar_borrar_empleado, name='confirmar_borrar_empleado'),
]


