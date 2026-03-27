from django.shortcuts import render

from .services import build_catalog_page


def product_catalog(request):
    catalog_page = build_catalog_page(
        data=request.GET or None,
        page_number=request.GET.get("page"),
    )

    return render(
        request,
        "products/catalog.html",
        {
            "form": catalog_page.form,
            "page_obj": catalog_page.page_obj,
            "products": catalog_page.products,
            "search_query": catalog_page.search_query,
        },
    )
