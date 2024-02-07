from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserForm
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

@login_required
def index(request):
    users = User.objects.all().order_by("-id")

    context = {
        "users": users
    }

    return render(request, "users/index.html", context)

@login_required
def create(request):
    form_action = reverse("users:create")
    
    # POST
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "O usuário foi cadastrado com sucesso!")

            return redirect("users:index")

        context = {
            "form": form,
            "form_action": form_action
        }

        return render(request, "users/create.html", context)
    # GET
    form = UserForm()

    context = {
        "form": form,
        "form_action": form_action
    }
    return render(request, "users/create.html", context)

@login_required
def update(request):
    return render(request, "users/create.html")

@login_required
def delete(request, id):
    user = get_object_or_404(User, id=id)

    user.delete()

    return redirect("users:index")

class UserLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True
    next_page = "products:index"

class UserLogoutView(LogoutView):
    next_page = "users:login"