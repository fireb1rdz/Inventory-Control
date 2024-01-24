from django import forms
from .models import Product
import re

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

        error_messages = {
            "name": {
                "unique": "O produto já existe.",
                "max_length": "O tamanho máximo do nome é 255 caracteres."
            }
        }