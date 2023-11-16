from django import forms
from .models import Cita, Mascota, Cliente
from datetime import time
from datetime import datetime, time
from django.utils import timezone
from pytz import timezone as tz
from django.core.exceptions import ValidationError
import pytz

HORARIO_CHOICES = [(time(hour, minute).strftime('%H:%M'), time(hour, minute).strftime('%I:%M %p')) for hour in range(9, 22) for minute in [0, 30]]


class CitaForm(forms.ModelForm):
    hora = forms.ChoiceField(choices=HORARIO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    cliente_username = forms.CharField(
        label='Cliente',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Cita
        fields = ['cliente_username', 'veterinario', 'mascota', 'fecha', 'hora', 'motivo']
        widgets = {
            'veterinario': forms.Select(attrs={'class': 'form-control'}),
            'mascota': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'motivo': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_cliente_username(self):
        username = self.cleaned_data.get('cliente_username')
        if username:
            try:
                cliente = Cliente.objects.get(user__username=username)
                return cliente
            except Cliente.DoesNotExist:
                raise forms.ValidationError("Cliente no encontrado. Asegúrese de ingresar un nombre de usuario válido.")
        else:
            raise forms.ValidationError("Este campo es requerido.")

    def clean(self):
        cleaned_data = super().clean()
        # Aquí puedes agregar otras validaciones
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        cliente_username = self.cleaned_data.get('cliente_username')
        if cliente_username:
            instance.cliente = Cliente.objects.get(user__username=cliente_username)
        
        if commit:
            instance.save()
            self.save_m2m()
        return instance

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['mascota'].queryset = Mascota.objects.none()
        if user and hasattr(user, 'cliente'):
            self.fields['cliente_username'].initial = user.username
            self.fields['mascota'].queryset = Mascota.objects.filter(cliente=user.cliente)
            self.fields['cliente_username'].widget = forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})

        if 'cliente_username' in self.data:
            try:
                cliente_id = Cliente.objects.get(user__username=self.data.get('cliente_username')).id
                self.fields['mascota'].queryset = Mascota.objects.filter(cliente_id=cliente_id).order_by('nombre')
            except (ValueError, TypeError, Cliente.DoesNotExist):
                pass  # Cliente inválido o no encontrado

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora_str = cleaned_data.get('hora')

        if fecha and hora_str:
            hora = datetime.strptime(hora_str, '%H:%M').time()
            fecha_hora_seleccionada = datetime.combine(fecha, hora)
            local_timezone = pytz.timezone('America/Santiago')
            fecha_hora_seleccionada = local_timezone.localize(fecha_hora_seleccionada)
            now = datetime.now(local_timezone)

            if fecha_hora_seleccionada < now:
                self.add_error('fecha', 'No puedes seleccionar una hora en una fecha anterior a hoy.')

            veterinario = cleaned_data.get('veterinario')
            citas_existente = Cita.objects.filter(veterinario=veterinario, fecha=fecha, hora=hora)
            if self.instance and self.instance.pk:
                citas_existente = citas_existente.exclude(pk=self.instance.pk)

            if citas_existente.exists():
                self.add_error('hora', 'Ya hay una cita agendada para este veterinario en la misma fecha y hora.')

        return cleaned_data

class EditarCitaForm(forms.ModelForm):
    hora = forms.ChoiceField(choices=HORARIO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Cita
        fields = ['veterinario','fecha', 'hora', 'motivo', 'estado']
        widgets = {
            'veterinario': forms.Select(attrs={'class': 'form-control'}),
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
        # Restringir el campo 'estado' si el usuario es un cliente
        if self.user and hasattr(self.user, 'cliente'):
            self.fields['cliente'].widget.attrs['readonly'] = True
            self.fields['cliente'].initial = self.user.username
            # Establecer 'Sin atender' como único valor para el campo 'estado'
            self.fields['estado'].choices = [('Sin atender', 'Sin atender')]
        elif self.user and hasattr(self.user, 'empleado') and self.user.empleado.rol in ['Administrador', 'Recepcionista']:
            # Dejar todas las opciones si el usuario es un empleado con el rol adecuado
            self.fields['estado'].choices = Mascota.ESTADO_MASCOTA_CHOICES

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

