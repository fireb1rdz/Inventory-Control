from django.db import models
from products.models import Product
from suppliers.models import Supplier

class Transactions(models.Model):
    TRANSACTION_CHOICES = {
            "E": "Entrada",
            "S": "Saída"
    }

    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_CHOICES)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=255, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)