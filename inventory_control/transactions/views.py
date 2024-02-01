from django.shortcuts import render
from .models import Transactions
from django.core.paginator import Paginator

def index(request):
    transactions = Transactions.objects.order_by("-date")

    paginator = Paginator(transactions, 100)
    page_number = paginator.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "transactions": page_obj
    }

    return render(request, "transactions/index.html", context)