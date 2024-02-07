from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, SupplierProduct, ProductInventory
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q 
from django.http import JsonResponse
from django.urls import reverse
from .forms import ProductForm, CategoryForm
from django.contrib import messages
from .forms import SupplierProductFormSet, ProductInventoryFormSet

# Create your views here.
def index(request):
    products = Product.objects.order_by("-id")
    product_inventory = ProductInventory.objects.order_by("-id")

    # Aplicando a paginação
    paginator = Paginator(products, 100)
    # /fornecedores?page=1 -> Obtendo a página da URL
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "product_inventory": product_inventory
        }
    
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
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            product = form.save()
            
            supplier_product_formset = SupplierProductFormSet(request.POST, instance=product)
            product_inventory_formset = ProductInventoryFormSet(request.POST, instance=product)
            
            if not supplier_product_formset.is_valid():                      
                messages.error(request, "Falha ao cadastrar os fornecedores do produto")
                product.delete()
                
                supplier_product_formset = SupplierProductFormSet(request.POST)
                product_inventory_formset = ProductInventoryFormSet(request.POST, instance=product)
        
                context = { 
                    "form": form, 
                    "supplier_product_formset": supplier_product_formset, 
                    "form_action": form_action,
                    "product_inventory_formset": product_inventory_formset}
                
                return render(request, "products/create.html", context)
            
            if product_inventory_formset.is_valid():
                messages.success(request, "O produto foi cadastrado com sucesso!")
                supplier_product_formset.save()
                product_inventory_formset.save()
            else:
                messages.error(request, "Falha ao cadastrar o estoque do produto")
                product.delete()
                supplier_product_formset = SupplierProductFormSet(request.POST)
                product_inventory_formset = ProductInventoryFormSet(request.POST, instance=product)
        
                context = { 
                    "form": form, 
                    "supplier_product_formset": supplier_product_formset, 
                    "form_action": form_action,
                    "product_inventory_formset": product_inventory_formset}
                
                return render(request, "products/create.html", context)
            
            return redirect("products:index")
                
        messages.error(request, "Falha ao cadastrar o produto. Verifique o preenchimento dos campos.")
        
        supplier_product_formset = SupplierProductFormSet(request.POST)
        
        context = { "form": form, "supplier_product_formset": supplier_product_formset, "form_action": form_action }
        
        return render(request, "products/create.html", context)

    # GET
    form = ProductForm()
    supplier_product_formset = SupplierProductFormSet()
    product_inventory_formset = ProductInventoryFormSet()

    context = {
        "form": form, 
        "form_action": form_action,
        "supplier_product_formset": supplier_product_formset,
        "product_inventory_formset": product_inventory_formset
        }

    return render(request, "products/create.html", context)

def update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form_action = reverse("products:update", args=(slug,))
    supplier_product_formset = SupplierProductFormSet(request.POST, instance=product)

    # POST
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            if form.cleaned_data["photo"] is False:
                product.thumbnail.delete()
            form.save()

            try:
                if supplier_product_formset.is_valid():
                    supplier_product_formset.save()
                    messages.success(request, "O produto foi atualizado com sucesso!")
                    return redirect("products:index")
                else:
                    messages.error(request, "Não é possível atualizar o produto. Verifique os campos de fornecedor")
                    
                    supplier_product_formset = SupplierProductFormSet(instance=product)

                    context = {
                    "form": form,
                    "supplier_product_formset": supplier_product_formset,
                    "form_action": form_action
                }

                return render(request, "products/create.html", context)

            except IntegrityError:
                messages.error(request, "Não é possível cadastrar o mesmo fornecedor para o mesmo produto.")

                context = {
                    "form": form,
                    "supplier_product_formset": supplier_product_formset,
                    "form_action": form_action
                }

                return render(request, "products/create.html", context)
        
        context = {
            "form_action": form_action,
            "supplier_product_formset": supplier_product_formset,
            "form": form
        }

        return render(request, "products/create.html", context)
    
    # GET
    form =  ProductForm(instance=product)
    supplier_product_formset = SupplierProductFormSet(instance=product)

    context = {
        "form_action": form_action,
        "form": form,
        "supplier_product_formset": supplier_product_formset
    }

    return render(request, "products/create.html", context)

@require_POST
def delete(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()

    return redirect("products:index")

@require_POST
def toggle_enabled(request, id):
    product = get_object_or_404(Product, pk=id)

    product.enabled = not product.enabled
    product.save()
    
    return JsonResponse({ "message": "success" })

def index_category(request):
    categories = Category.objects.order_by("-id")

    paginator = Paginator(categories, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "categories": page_obj
    }

    return render(request, "categories/index.html", context)

def search_category(request):
    # Obtendo o valor da requisição (Formulário)
    search_value = request.GET.get("q").strip()

    # Verificando se algo foi digitado
    if not search_value:
        return redirect("products:index_category")
    
    # Filtrando os produtos
    #  O Q é usado para combinar filtros (& ou |)
    products = Category.objects\
        .filter(Q(name__icontains=search_value) | Q(category__name__icontains=search_value))\
        .order_by("-id")

    paginator = Paginator(products, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = { "products": page_obj}

    return render(request, "categories/index.html", context)

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

def update_category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    # POST
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria atualizada com sucesso!")
            return redirect("products:index_category")
        
        context = {
            "form": form
        }

        return render(request, "category/create.html", context)
    
    # GET
    form =  CategoryForm(instance=category)

    context = {
        "form": form
    }

    return render(request, "categories/create.html", context)

@require_POST
def delete_supplier_from_product(request, id):
    supplier_product = get_object_or_404(SupplierProduct, pk=id)
    supplier_product.delete()

    return JsonResponse({"message": "success"})

@require_POST
def delete_category(request, id):
    supplier = get_object_or_404(Category, pk=id)
    supplier.delete()

    return redirect("products:index_category")

@require_GET
def get_suppliers_from_product(request, id):
    suppliers = SupplierProduct.objects.filter(product__id=id).order_by("-id")

    # Serialização
    suppliers_serialized = [{
        "id": supplierProduct.id,
        "name": supplierProduct.supplier.fantasy_name,
        "cost_price": supplierProduct.cost_price
    } for supplierProduct in suppliers] 

    return JsonResponse(suppliers_serialized, safe=False)
