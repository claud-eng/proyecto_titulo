from django import forms
from .models import Ficha

class FichaForm(forms.ModelForm):
    class Meta:
        model = Ficha
        fields = ['cliente', 'mascota', 'veterinario', 'fecha', 'medicamento', 'dosis', 'instrucciones']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'mascota': forms.Select(attrs={'class': 'form-control'}),
            'veterinario': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'medicamento': forms.TextInput(attrs={'class': 'form-control'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control'}),
            'instrucciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(FichaForm, self).__init__(*args, **kwargs)
        # Agregar una opción vacía al campo cliente
        self.fields['cliente'].empty_label = "---------"

        # Opcional: Puedes deshabilitar la opción vacía si no deseas que sea seleccionable
        # self.fields['cliente'].required = True
