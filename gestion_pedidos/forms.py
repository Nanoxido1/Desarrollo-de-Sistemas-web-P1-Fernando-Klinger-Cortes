from django import forms
from django.utils import timezone
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre_cliente', 'email_cliente', 'modalidad', 'producto', 'fecha_entrega', 'direccion', 'total_estimado', 'observaciones']
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'email_cliente': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'modalidad': forms.Select(attrs={'class': 'form-select'}),
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'fecha_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'total_estimado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto total en CLP'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_entrega = cleaned_data.get('fecha_entrega')
        modalidad = cleaned_data.get('modalidad')
        total_estimado = cleaned_data.get('total_estimado')
        observaciones = cleaned_data.get('observaciones')
        producto = cleaned_data.get('producto')

        # 1. Validación de Fechas (No anterior a la fecha actual)
        if fecha_entrega and fecha_entrega < timezone.now().date():
            self.add_error('fecha_entrega', 'La fecha de entrega programada no puede ser previa a la fecha actual.')

        # 2. Restricción Despacho Express ($15.000 CLP mínimo)
        if modalidad == 'EXPRESS' and total_estimado is not None:
            if total_estimado < 15000:
                self.add_error('total_estimado', 'El monto mínimo para Despacho Express es de $15.000 CLP.')

        # 3. Control de Productos Refrigerados (Bolsa térmica requerida en Pickup)
        if producto and producto.requiere_refrigeracion and modalidad == 'PICKUP':
            if not observaciones or ('bolsa termica' not in observaciones.lower() and 'bolsa térmica' not in observaciones.lower()):
                self.add_error('observaciones', 'Para productos refrigerados con Retiro en Tienda, se debe indicar "bolsa térmica" en las observaciones.')

        return cleaned_data