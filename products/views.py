from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Product


def product_catalog(request):
    products_qs = Product.objects.order_by("name", "id")
    paginator = Paginator(products_qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "products/catalog.html",
        {
            "page_obj": page_obj,
            "products": page_obj.object_list,
        },
    )
