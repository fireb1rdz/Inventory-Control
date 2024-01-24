import os
from django.db import models
from django.utils.text import slugify
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    sale_price = models.FloatField()
    is_perishable = models.BooleanField()
    expiration_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="product-images", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="thumbnails", blank=True, null=True)
    enabled = models.BooleanField(default=True)

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
        
        img = Image.open(self.photo.path) # Abrindo a imagem com o pillow
        size = (30, 30) # Definindo o tamanho do redimensionamento
        img.thumbnail(size) # Redimensionando a imagem

        # Salvando a imagem
        thumb_io = BytesIO()
        img.save(thumb_io, img.format, quality=85)

        name, extension = os.path.splitext(self.photo.name) # [nome-arquivo, .jpeg]
        thumb_filename = f"{name}_thumb{extension}"

        # Salvar a imagem na instância do produto
        self.thumbnail.save(thumb_filename, ContentFile(thumb_io.getvalue()), save=False)

    def __delete_file_if_exists(self, file):
        if file and os.path.isfile(file.path):
            os.remove(file.path)

    def delete(self, *args, **kwargs):
        self.__delete_file_if_exists(self.photo)
        super(Product, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"