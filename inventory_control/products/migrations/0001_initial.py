# Generated by Django 5.0.1 on 2024-01-23 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('sale_price', models.FloatField()),
                ('is_perishable', models.BooleanField()),
                ('expiration_date', models.DateField(blank=True)),
                ('photo', models.ImageField(upload_to='product-images')),
                ('enabled', models.BooleanField()),
            ],
        ),
    ]
