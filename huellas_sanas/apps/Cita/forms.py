from django import forms
from .models import Cita, Mascota, Cliente
from datetime import time
from datetime import datetime, time
from django.utils import timezone
from pytz import timezone as tz
from django.core.exceptions import ValidationError

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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super(CitaForm, self).__init__(*args, **kwargs)

        if user and hasattr(user, 'cliente'):
            self.fields['cliente'].queryset = Cliente.objects.filter(user=user.cliente.user)
            self.fields['mascota'].queryset = Mascota.objects.filter(cliente=user.cliente)


        if user and hasattr(user, 'cliente'):
            self.fields['cliente'].queryset = Cliente.objects.filter(user=user.cliente.user)

            # Verificar si el cliente tiene mascotas asociadas
            mascotas = Mascota.objects.filter(cliente=user.cliente)
            if mascotas.exists():
                self.fields['mascota'].queryset = mascotas
            else:
                # Si el cliente no tiene mascotas, muestra un mensaje personalizado en el widget
                self.fields['mascota'].widget = forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Antes de poder agendar una cita, primero debe tener una mascota asociada a su cuenta. Puede agregar una en la sección Revisar estado de mi mascota.',
                    'readonly': True,  # Establecer el campo como solo lectura
                })
                
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora_str = cleaned_data.get('hora')  # Obtener la hora como cadena

        if fecha and hora_str:
            hora = datetime.strptime(hora_str, '%H:%M').time()  # Convertir la cadena en objeto datetime.time
            fecha_hora_seleccionada = datetime.combine(fecha, hora)
            
            # Convertir a la zona horaria local (por ejemplo, 'America/Bogota')
            local_timezone = tz('America/Santiago')
            fecha_hora_seleccionada = local_timezone.localize(fecha_hora_seleccionada)
            now = timezone.localtime(timezone.now())  # Obtener la hora actual en la zona horaria local

            if fecha_hora_seleccionada < now:
                raise forms.ValidationError('No puedes seleccionar una hora en una fecha anterior a hoy.')

        veterinario = cleaned_data.get('veterinario')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if veterinario and fecha and hora:
            # Verificar si ya existe una cita para el mismo veterinario en la misma fecha y hora
            citas_existente = Cita.objects.filter(veterinario=veterinario, fecha=fecha, hora=hora)

            if self.instance:
                # Si estamos editando una cita existente, excluimos esta cita de la consulta
                citas_existente = citas_existente.exclude(pk=self.instance.pk)

            if citas_existente.exists():
                # Si hay una cita existente, muestra un error de validación
                raise forms.ValidationError('Ya hay una cita agendada para este veterinario en la misma fecha y hora.')

        return cleaned_data

class EditarCitaForm(forms.ModelForm):
    hora = forms.ChoiceField(choices=HORARIO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
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
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora_str = cleaned_data.get('hora')  # Obtener la hora como cadena

        if fecha and hora_str:
            hora = datetime.strptime(hora_str, '%H:%M').time()  # Convertir la cadena en objeto datetime.time
            fecha_hora_seleccionada = datetime.combine(fecha, hora)
            
            # Convertir a la zona horaria local (por ejemplo, 'America/Bogota')
            local_timezone = tz('America/Santiago')
            fecha_hora_seleccionada = local_timezone.localize(fecha_hora_seleccionada)
            now = timezone.localtime(timezone.now())  # Obtener la hora actual en la zona horaria local

            if fecha_hora_seleccionada < now:
                raise forms.ValidationError('No puedes seleccionar una hora en una fecha anterior a hoy.')

        veterinario = cleaned_data.get('veterinario')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if veterinario and fecha and hora:
            # Verificar si ya existe una cita para el mismo veterinario en la misma fecha y hora
            citas_existente = Cita.objects.filter(veterinario=veterinario, fecha=fecha, hora=hora)

            if self.instance:
                # Si estamos editando una cita existente, excluimos esta cita de la consulta
                citas_existente = citas_existente.exclude(pk=self.instance.pk)

            if citas_existente.exists():
                # Si hay una cita existente, muestra un error de validación
                raise forms.ValidationError('Ya hay una cita agendada para este veterinario en la misma fecha y hora.')

        return cleaned_data

class MascotaForm(forms.ModelForm):
    cliente = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MascotaForm, self).__init__(*args, **kwargs)
        if self.user and hasattr(self.user, 'cliente'):
            self.fields['cliente'].widget.attrs['readonly'] = True
            self.fields['cliente'].initial = self.user.username

    class Meta:
        model = Mascota
        fields = ['cliente', 'nombre', 'especie', 'raza', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.Select(attrs={'class': 'form-control', 'id': 'id_especie'}),
            'raza': forms.Select(attrs={'class': 'form-control', 'id': 'id_raza'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        return nombre.capitalize()

    def clean_cliente(self):
        username_cliente = self.cleaned_data.get('cliente')
        try:
            cliente = Cliente.objects.get(user__username=username_cliente)
        except Cliente.DoesNotExist:
            raise ValidationError(f"Cliente con nombre de usuario '{username_cliente}' no existe.")
        return cliente

class EditarMascotaForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditarMascotaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.Select(attrs={'class': 'form-control', 'id': 'id_especie'}),
            'raza': forms.Select(attrs={'class': 'form-control', 'id': 'id_raza'}),  
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        return nombre.capitalize()

