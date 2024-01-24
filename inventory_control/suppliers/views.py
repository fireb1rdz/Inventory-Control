from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.db.models import Q 
from django.http import JsonResponse
from django.urls import reverse
from .forms import SupplierForm
from django.contrib import messages

# Create your views here.
def index(request):
    suppliers = Supplier.objects.order_by("-id")

    # Aplicando a paginação
    paginator = Paginator(suppliers, 100)
    # /fornecedores?page=1 -> Obtendo a página da URL
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"suppliers": page_obj}
    return render(request, "suppliers/index.html", context)

def search(request):
    # Obtendo o valor da requisição (Formulário)
    search_value = request.GET.get("q").strip()

    # Verificando se algo foi digitado
    if not search_value:
        return redirect("suppliers:index")
    
    # Filtrando os fornecedores
    #  O Q é usado para combinar filtros (& ou |)
    suppliers = Supplier.objects.filter(Q(fantasy_name__icontains=search_value) | 
                                        Q(company_name__icontains=search_value)) \
                                        .order_by("-id")

    paginator = Paginator(suppliers, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = { "suppliers": page_obj}

    return render(request, "suppliers/index.html", context)

def create(request):
    form_action = reverse("suppliers:create")
    # POST

    if request.method == "POST":
        form = SupplierForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "O fornecedor foi cadastrado com sucesso!")
            return redirect("suppliers:index")
        
        messages.error(request, "Falha ao cadastrar o fornecedor. Verifique o preenchimento dos campos.")
        
        context = { "form": form, "form_action": form_action}

        return render(request, "suppliers/create.html", context)

    # GET
    form = SupplierForm()

    context = {"form": form, "form_action": form_action}

    return render(request, "suppliers/create.html", context)

def update(request, slug):
    supplier = get_object_or_404(Supplier, slug=slug)
    form_action = reverse("suppliers:update", args=(slug,))

    # POST
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, "Fornecedor atualizado com sucesso!")
            return redirect("suppliers:index")
        
        context = {
            "form_action": form_action,
            "form": form
        }

        return render(request, "suppliers/create.html", context)
    
    # GET
    form =  SupplierForm(instance=supplier)

    context = {
        "form_action": form_action,
        "form": form
    }

    return render(request, "suppliers/create.html", context)

@require_POST
def delete(request, id):
    supplier = get_object_or_404(Supplier, pk=id)
    supplier.delete()

    return redirect("suppliers:index")

@require_POST
def toggle_enabled(request, id):
    supplier = get_object_or_404(Supplier, pk=id)

    supplier.enabled = not supplier.enabled
    supplier.save()
    
    return JsonResponse({ "message": "sucess" })
    