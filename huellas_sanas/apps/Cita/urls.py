from django.urls import path, include  # Importa path para definir rutas de URL e include para incluir otras configuraciones de URL
from . import views  # Importa las vistas definidas en el directorio actual (directorio donde se encuentra este archivo)

urlpatterns = [
    # Rutas para las citas
    # Listar las citas agendadas de la bd
    path('listar_citas', views.listar_citas, name="listar_citas"),
    # Agregar una cita
    path('agendar_cita', views.agendar_cita, name="agendar_cita"),
    # Le avise al usuario de que debe estar logeado para agendar una cita
    path('agendar_cita_sin_login', views.agendar_cita_sin_login, name="agendar_cita_sin_login"),
    # Editar una cita
    path('editar_cita/<int:cita_id>', views.editar_cita, name="editar_cita"),
    # Borrar una cita
    path('borrar_cita/<int:cita_id>', views.borrar_cita, name="borrar_cita"),
    # Confirmar antes de borrar una cita
    path('confirmar-borrar-cita/<int:cita_id>/', views.confirmar_borrar_cita, name='confirmar_borrar_cita'),
    path('confirmar-cancelar-cita/<int:cita_id>/', views.confirmar_cancelar_cita, name='confirmar_cancelar_cita'),

    # Listar las mascotas de la bd
    path('listar_mascotas', views.listar_mascotas, name="listar_mascotas"),
    # Agregar un empleado
    path('agregar_mascota', views.agregar_mascota, name="agregar_mascota"),
    # Editar un empleado
    path('editar_mascota/<int:mascota_id>', views.editar_mascota, name="editar_mascota"),
    # Borrar un empleado
    path('borrar_mascota/<int:mascota_id>', views.borrar_mascota, name="borrar_mascota"),
    # Confirmar antes de borrar un empleado
    path('confirmar-borrar-mascota/<int:mascota_id>/', views.confirmar_borrar_mascota, name='confirmar_borrar_mascota'),
]
