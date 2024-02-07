from django.urls import path
from . import views
from .views import SupplierListView, SupplierSearchView, SupplierCreateView, SupplierUpdateView, SupplierDeleteView

app_name = "suppliers"
urlpatterns = [
    path("", SupplierListView.as_view(), name="index"),
    path("cadastro", SupplierCreateView.as_view(), name="create"),
    path("<int:pk>/delete", SupplierDeleteView.as_view(), name="delete"), # fornecedores/1/delete
    path("search", SupplierSearchView.as_view(), name="search"),
    path("<int:id>/toggle_enabled", views.toggle_enabled, name="toggle_enabled"),
    path("<slug:slug>", SupplierUpdateView.as_view(), name="update")
]
