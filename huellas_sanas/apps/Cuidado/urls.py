from django.urls import path
from . import views

urlpatterns = [
    # Rutas para fichas
    path('listar_fichas', views.listar_fichas, name="listar_fichas"),
    path('agregar_ficha', views.agregar_ficha, name="agregar_ficha"),
    path('editar_ficha/<int:ficha_id>', views.editar_ficha, name="editar_ficha"),
    path('borrar_ficha/<int:ficha_id>', views.borrar_ficha, name="borrar_ficha"),
    path('confirmar-borrar-ficha/<int:ficha_id>/', views.confirmar_borrar_ficha, name='confirmar_borrar_ficha'),
]