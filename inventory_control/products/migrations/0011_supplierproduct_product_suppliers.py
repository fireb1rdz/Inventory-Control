# Generated by Django 5.0.1 on 2024-01-29 22:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_category_slug'),
        ('suppliers', '0002_alter_supplier_options_rename_phone_supplier_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suppliers.supplier')),
            ],
            options={
                'verbose_name': 'Fornecedor do Produto',
                'verbose_name_plural': 'Fornecedores do Produto',
                'unique_together': {('supplier', 'product')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='suppliers',
            field=models.ManyToManyField(through='products.SupplierProduct', to='suppliers.supplier'),
        ),
    ]