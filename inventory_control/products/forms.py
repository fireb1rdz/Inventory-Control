from django import forms
from .models import Product, Category
import re

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["thumbnail", "slug", "is_perishable"]

        labels = {
            "name": "Nome",
            "description": "Descrição",
            "sale_price": "Preço de venda",
            "expiration_date": "Data de expiração",
            "photo": "Imagem do produto",
            "enabled": "Ativo",
            "category": "Categoria"
        }

        error_messages = {
            "name": {
                "required": "O campo nome é obrigatório",
                "unique": "Já existe um produto cadastrado com esse nome"
            },
            "description": {
                "required": "O campo descrição é obrigatório"
            },
            "sale_price": {
                "required": "O campo preço de venda é obrigatório",
            },
        }

        widgets = {
            "expiration_date": forms.DateInput(attrs={"type":"date"}, format="%Y-%m-%d")
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

        labels = {
            "name": "Nome",
            "description": "Descrição",
        }

        error_messages = {
            "name": {
                "required": "O campo nome é obrigatório",
                "unique": "Já existe uma categoria cadastrada com esse nome"
            },
            "description": {
                "required": "O campo descrição é obrigatório"
            },
        }

