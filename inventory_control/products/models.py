import os
from django.db import models
from django.utils.text import slugify
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from suppliers.models import Supplier

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    sale_price = models.FloatField()
    is_perishable = models.BooleanField()
    expiration_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="product-images", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="thumbnails", blank=True, null=True)
    enabled = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    suppliers = models.ManyToManyField(
        Supplier,
        through="SupplierProduct",
        through_fields=("product", "supplier"),
        blank=True
    )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.__update_is_perishable()
        
        super(Product, self).save(*args, **kwargs)
        
        self.__create_thumbnail()
        super(Product, self).save(*args, **kwargs)

    def __update_is_perishable(self):
        self.is_perishable = bool(self.expiration_date)

    def __create_thumbnail(self):
        if not self.photo:
            return
        
        img = Image.open(self.photo) # Abrindo a imagem com o pillow
        size = (30, 30) # Definindo o tamanho do redimensionamento
        img.thumbnail(size) # Redimensionando a imagem
        extension = f".{img.format.lower()}"

        # Salvando a imagem
        thumb_io = BytesIO()
        img.save(thumb_io, img.format, quality=85)

        # Salvar a imagem na instância do produto
        self.thumbnail.save(f"{self.slug}_thumb{extension}", ContentFile(thumb_io.getvalue()), save=False)

    def __delete_file_if_exists(self, file):
        if file and os.path.isfile(file.path):
            os.remove(file.path)

    def delete(self, *args, **kwargs):
        self.__delete_file_if_exists(self.photo)
        super(Product, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"


class SupplierProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    cost_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Fornecedor do Produto"
        verbose_name_plural = "Fornecedores do Produto"
        unique_together = [["supplier", "product"]]

class ProductInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    local = models.CharField(max_length=255)
    

    def __str__(self):
        return f"Produto: {self.product.name} | Quantidade: {self.quantity}"
    class Meta:
        verbose_name = "Inventário de produto"
        verbose_name_plural = "Inventário de produtos"
        unique_together = [["product", "local"]]