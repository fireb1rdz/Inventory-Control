from django import forms
from .models import Product, Category, SupplierProduct
import re
from crispy_forms.helper import FormHelper

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
                "unique": "Já existe um produto cadastrado com esse nome",
                "required": "O campo nome é obrigatório"
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

class SupplierProductForm(forms.ModelForm):
    class Meta:
        model = SupplierProduct
        exclude = ["product"]
        widgets = {
            "cost_price": forms.NumberInput(attrs={"placeholder": "Preço de custo"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

SupplierProductFormSet = forms.inlineformset_factory(
    Product,
    SupplierProduct,
    form=SupplierProductForm,
    extra=1,
    can_delete=True,
    max_num=5
)