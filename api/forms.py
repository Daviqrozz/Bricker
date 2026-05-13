from django import forms
from .models import Product, Sale

INPUT_CLASSES = 'form-control bg-card text-primary'
SELECT_CLASSES = 'form-select bg-card flex-grow-1'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'observation', 'category', 'cost', 'expected_sale_value']
        exclude = ['user']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Nome do Produto'}),
            'category': forms.Select(attrs={'class': SELECT_CLASSES, 'required': True}),
            'cost': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Ex: R$ 50,00', 'min': 0, 'step': '0.01'}),
            'expected_sale_value': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Ex: R$ 80,00 - Opcional', 'min': 0, 'step': '0.01'}),
            'observation': forms.Textarea(attrs={'class': INPUT_CLASSES, 'placeholder': 'Observações', 'rows': 3}),
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'price_sold']
        widgets = {
            'product': forms.Select(attrs={'class': SELECT_CLASSES, 'required': True}),
            'price_sold': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Valor de Venda (R$)', 'min': 0, 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['product'].queryset = Product.objects.filter(
                user=user,
                status=Product.Status.AVAILABLE
            )