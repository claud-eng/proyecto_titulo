from django import forms
from .models import Producto, Servicio

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'descripcion', 'precio', 'cantidad_stock']
        # Define los widgets y atributos de clase según tus necesidades

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio']
        # Define los widgets y atributos de clase según tus necesidades
