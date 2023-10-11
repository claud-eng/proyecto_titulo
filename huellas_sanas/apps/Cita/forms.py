from django import forms
from .models import Cita, Mascota, Cliente
from datetime import time
from datetime import datetime, time
from django.utils import timezone
from pytz import timezone as tz

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

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        # Asegúrate de que el nombre tenga la primera letra en mayúscula y el resto en minúscula
        return nombre.capitalize()
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtener el usuario actual de los argumentos

        super(MascotaForm, self).__init__(*args, **kwargs)

        if user:
            # Verificar si el usuario es un cliente
            if user.cliente:
                # Si es un cliente, establecer el queryset del campo de Cliente para mostrar solo su propio cliente
                self.fields['cliente'].queryset = Cliente.objects.filter(user=user.cliente.user)
                self.fields['estado'].widget.choices = [('Sin atender', 'Sin atender')]
            elif user.empleado and user.empleado.rol in ['Administrador', 'Recepcionista']:
                # Si es un empleado con roles permitidos, mostrar todos los clientes en el queryset
                self.fields['cliente'].queryset = Cliente.objects.all()

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

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        # Asegúrate de que el nombre tenga la primera letra en mayúscula y el resto en minúscula
        return nombre.capitalize()

