from django import forms
from .models import Producto, Servicio

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'descripcion', 'precio', 'cantidad_stock']
        # Define los widgets y atributos de clase según tus necesidades

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        marca = cleaned_data.get('marca')
        descripcion = cleaned_data.get('descripcion')

        if nombre:
            cleaned_data['nombre'] = nombre.capitalize()
        if marca:
            cleaned_data['marca'] = marca.capitalize()
        if descripcion:
            cleaned_data['descripcion'] = descripcion.capitalize()

        return cleaned_data

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio']
        # Define los widgets y atributos de clase según tus necesidades

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        descripcion = cleaned_data.get('descripcion')

        if nombre:
            cleaned_data['nombre'] = nombre.capitalize()
        if descripcion:
            cleaned_data['descripcion'] = descripcion.capitalize()

        return cleaned_data