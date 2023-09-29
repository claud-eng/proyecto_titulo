from django import forms
from .models import Cita, Mascota
from datetime import time

HORARIO_CHOICES = [(time(hour, minute).strftime('%H:%M'), time(hour, minute).strftime('%I:%M %p')) for hour in range(9, 22) for minute in [0, 30]]

class CitaForm(forms.ModelForm):
    hora = forms.ChoiceField(choices=HORARIO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Cita
        fields = ['cliente', 'veterinario', 'mascota', 'fecha', 'hora', 'motivo']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'veterinario': forms.Select(attrs={'class': 'form-control'}),
            'mascota': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'motivo': forms.Select(attrs={'class': 'form-control'}),
        }

class EditarCitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['cliente', 'veterinario', 'mascota', 'fecha', 'hora', 'motivo', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'veterinario': forms.Select(attrs={'class': 'form-control'}),
            'mascota': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.Select(choices=HORARIO_CHOICES, attrs={'class': 'form-control'}),
            'motivo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(choices=Cita.ESTADO_CHOICES, attrs={'class': 'form-control'}),
        }

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['cliente', 'nombre', 'especie', 'raza']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.Select(attrs={'class': 'form-control'}),
            'raza': forms.Select(attrs={'class': 'form-control'}),
        }

def __init__(self, *args, **kwargs):
    super(MascotaForm, self).__init__(*args, **kwargs)
    
    # Obtener las opciones de raza según la especie seleccionada
    especie = self.initial.get('especie')  # Obtener el valor inicial de 'especie'

    if especie:
        razas_choices = dict(self.fields['especie'].choices)  # Obtener las opciones de raza desde el formulario
        razas = razas_choices.get(especie, [])  # Obtener las razas para la especie seleccionada
        self.fields['raza'].choices = razas
    else:
        # Si no se ha seleccionado una especie, dejar las opciones de raza vacías
        self.fields['raza'].choices = []

class EditarMascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['cliente', 'nombre', 'especie', 'raza']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.TextInput(attrs={'class': 'form-control'}),
            'raza': forms.TextInput(attrs={'class': 'form-control'}),
        }

