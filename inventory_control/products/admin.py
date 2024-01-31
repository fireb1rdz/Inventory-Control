from django.contrib import admin
from .models import Product, Category, SupplierProduct, ProductInventory

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "sale_price", "is_perishable", "expiration_date", "enabled"]
    exclude = ["slug", "thumbnail"]
    search_fields = ["name"]
    list_display_links = ["name"]
    list_editable = ["sale_price", "is_perishable", "expiration_date"]
    list_per_page = 100
    list_max_show_all = 1000

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    list_display_links = ["name"]
    list_per_page = 100
    list_max_show_all = 1000

@admin.register(SupplierProduct)
class SupplierProductAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "supplier", "cost_price"]
    search_fields = ["product"]
    list_per_page = 100
    list_max_show_all = 1000

@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity", "local"]
    search_fields = ["product"]
    list_per_page = 100
    list_max_show_all = 1000


