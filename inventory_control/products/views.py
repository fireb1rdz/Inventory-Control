from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.db.models import Q 
from django.http import JsonResponse
from django.urls import reverse
from .forms import ProductForm, CategoryForm
from django.contrib import messages

# Create your views here.
def index(request):
    products = Product.objects.order_by("-id")

    # Aplicando a paginação
    paginator = Paginator(products, 100)
    # /fornecedores?page=1 -> Obtendo a página da URL
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"products": page_obj}
    return render(request, "products/index.html", context)

def search(request):
    # Obtendo o valor da requisição (Formulário)
    search_value = request.GET.get("q").strip()

    # Verificando se algo foi digitado
    if not search_value:
        return redirect("products:index")
    
    # Filtrando os produtos
    #  O Q é usado para combinar filtros (& ou |)
    products = Product.objects\
        .filter(Q(name__icontains=search_value) | Q(category__name__icontains=search_value))\
        .order_by("-id")

    paginator = Paginator(products, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = { "products": page_obj}

    return render(request, "products/index.html", context)

def create(request):
    form_action = reverse("products:create")
    # POST

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "O produto foi cadastrado com sucesso!")
            return redirect("products:index")
        
        messages.error(request, "Falha ao cadastrar o produto. Verifique o preenchimento dos campos.")
        
        context = { "form": form, "form_action": form_action}

        return render(request, "products/create.html", context)

    # GET
    form = ProductForm()

    context = {"form": form, "form_action": form_action}

    return render(request, "products/create.html", context)

def update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form_action = reverse("products:update", args=(slug,))

    # POST
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            if form.cleaned_data["photo"] is False:
                product.thumbnail.delete()
            form.save()
            messages.success(request, "Produto atualizado com sucesso!")
            return redirect("products:index")
        
        context = {
            "form_action": form_action,
            "form": form
        }

        return render(request, "products/create.html", context)
    
    # GET
    form =  ProductForm(instance=product)

    context = {
        "form_action": form_action,
        "form": form
    }

    return render(request, "products/create.html", context)

@require_POST
def delete(request, id):
    supplier = get_object_or_404(Product, pk=id)
    supplier.delete()

    return redirect("products:index")

@require_POST
def toggle_enabled(request, id):
    supplier = get_object_or_404(Product, pk=id)

    supplier.enabled = not supplier.enabled
    supplier.save()
    
    return JsonResponse({ "message": "sucess" })

def create_category(request):
    form_action = reverse("products:create_category")
    
    # POST
    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "A categoria foi cadastrada com sucesso!")
            return redirect("products:index")
        
        messages.error(request, "Falha ao cadastrar o produto. Verifique o preenchimento dos campos.")

        context = {
            "form_action": form_action,
            "form": form,
        }

        return render(request, "categories/create.html", context)
    
    form = CategoryForm()

    context = {
        "form_action": form_action,
        "form": form
    }

    return render(request, "categories/create.html", context)

def index_category(request):
    categories = Category.objects.order_by("-id")

    paginator = Paginator(categories, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "categories": page_obj
    }

    return render(request, "categories/index.html", context)