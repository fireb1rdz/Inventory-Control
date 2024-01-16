from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    suppliers = Supplier.objects.order_by("-id")

    context = {"suppliers": suppliers}
    return render(request, "index.html", context)

def delete(request, id):
    supplier = get_object_or_404(Supplier, pk=id)
    supplier.delete()

    return redirect("suppliers:index")