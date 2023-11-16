from django import forms
from apps.Cita.models import Mascota
from .models import Ficha
from apps.Usuario.models import Cliente

class FichaForm(forms.ModelForm):
    cliente_username = forms.CharField(
        label='Cliente',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Ficha
        exclude = ['cliente']
        widgets = {
            'mascota': forms.Select(attrs={'class': 'form-control'}),
            'veterinario': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'medicamento': forms.TextInput(attrs={'class': 'form-control'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control'}),
            'instrucciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean_cliente_username(self):
        username = self.cleaned_data.get('cliente_username')
        try:
            cliente = Cliente.objects.get(user__username=username)
            return cliente
        except Cliente.DoesNotExist:
            raise forms.ValidationError("Cliente no encontrado. Asegúrese de ingresar un nombre de usuario válido.")
        
    def save(self, commit=True):
        ficha = super().save(commit=False)
        username = self.cleaned_data.get('cliente_username')
        if username:
            cliente = Cliente.objects.get(user__username=username)
            ficha.cliente = cliente
        if commit:
            ficha.save()
            self.save_m2m()
        return ficha

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude_fields', [])
        super(FichaForm, self).__init__(*args, **kwargs)
        self.fields['mascota'].queryset = Mascota.objects.none()

        # Excluir campos si se especifican
        for field in exclude_fields:
            if field in self.fields:
                del self.fields[field]

        if 'cliente_username' in self.data:
            try:
                cliente_id = Cliente.objects.get(user__username=self.data.get('cliente_username')).id
                self.fields['mascota'].queryset = Mascota.objects.filter(cliente_id=cliente_id).order_by('nombre')
            except (ValueError, TypeError, Cliente.DoesNotExist):
                pass  # Cliente inválido o no encontrado
