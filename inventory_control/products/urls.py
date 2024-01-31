from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path("", views.index, name="index"),
    path("cadastro", views.create, name="create"),
    path("<int:id>/delete", views.delete, name="delete"), # fornecedores/1/delete
    path("search", views.search, name="search"),
    path("<int:id>/toggle_enabled", views.toggle_enabled, name="toggle_enabled"),
    path("<slug:slug>", views.update, name="update"),
    path("categorias/", views.index_category, name="index_category"),
    path("categorias/cadastro", views.create_category, name="create_category"),
    path("categories/<int:id>/delete", views.delete_category, name="delete_category"),
    path("categories/search", views.search_category, name="search_category"),
    path("categorias/<slug:slug>/", views.update_category, name="update_category"),
    path("<int:id>/suppliers/", views.get_suppliers_from_product, name="suppliers"),
    path("<int:id>/delete_supplier", views.delete_supplier_from_product, name="delete_supplier")
]

