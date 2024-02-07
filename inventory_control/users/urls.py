from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views import UserLoginView, UserLogoutView

app_name = "users"
urlpatterns = [
    path("", RedirectView.as_view(url="/login/", permanent=True)),
    path("usuarios/", views.index, name="index"),
    path("usuarios/cadastro/", views.create, name="create"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("usuarios/<str:username>/", views.update, name="update"),
    path("usuarios/<int:id>/delete", views.delete, name="delete"),
    path("logout/", views.UserLogoutView.as_view(), name="logout")
]
