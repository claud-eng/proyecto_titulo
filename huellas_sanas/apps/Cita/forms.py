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
        }

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['cliente', 'nombre', 'especie', 'raza', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.Select(attrs={'class': 'form-control', 'id': 'id_especie'}),
            'raza': forms.Select(attrs={'class': 'form-control', 'id': 'id_raza'}),  # Cambiar a Select
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

class EditarMascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['cliente', 'nombre', 'especie', 'raza', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.Select(attrs={'class': 'form-control', 'id': 'id_especie'}),
            'raza': forms.Select(attrs={'class': 'form-control', 'id': 'id_raza'}),  
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }



