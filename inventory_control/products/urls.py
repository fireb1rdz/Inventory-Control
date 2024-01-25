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
    path("categorias/index", views.index_category, name="index_category"),
    path("categorias/cadastro", views.create_category, name="create_category")
]

