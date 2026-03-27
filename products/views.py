from django.shortcuts import render

from .services import build_catalog_page


def product_catalog(request):
    per_page_val = request.GET.get("per_page", 24)

    try:
        per_page_val = int(per_page_val)
    except ValueError:
        per_page_val = 24

    catalog_page = build_catalog_page(
        data=request.GET or None,
        page_number=request.GET.get("page"),
        per_page=per_page_val,
    )

    return render(
        request,
        "products/catalog.html",
        {
            "form": catalog_page.form,
            "page_obj": catalog_page.page_obj,
            "products": catalog_page.products,
            "search_query": catalog_page.search_query,
            "page_range": catalog_page.page_range,
        },
    )
