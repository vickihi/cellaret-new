from django.shortcuts import get_object_or_404, render

from cellars.selectors import (
    get_cellar_product_bottle,
    get_user_cellars,
    get_user_cellar_or_404,
    get_user_default_cellar,
)
from .services import build_catalog_page

from .models import Product


def product_catalog(request):
    target_cellar = None
    cellar_id = request.GET.get("cellar_id")

    if cellar_id and request.user.is_authenticated:
        target_cellar = get_user_cellar_or_404(user=request.user, cellar_id=cellar_id)

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

    user_cellars = []
    if request.user.is_authenticated:
        user_cellars = list(get_user_cellars(user=request.user))

    return render(
        request,
        "products/catalog.html",
        {
            "form": catalog_page.form,
            "sort_form": catalog_page.sort_form,
            "filter_form": catalog_page.filter_form,
            "page_obj": catalog_page.page_obj,
            "products": catalog_page.products,
            "search_query": catalog_page.search_query,
            "sort_key": catalog_page.sort_key,
            "active_filters": catalog_page.active_filters,
            "available_filters": catalog_page.available_filters,
            "page_range": catalog_page.page_range,
            "breadcrumbs": catalog_page.breadcrumbs,
            "target_cellar": target_cellar,
            "cellars": user_cellars,
        },
    )


def product_detail(request, sku):
    product = get_object_or_404(Product, sku=sku)
    selected_cellar = None
    user_cellars = []
    product_bottles = []

    if request.user.is_authenticated:
        user_cellars = list(get_user_cellars(user=request.user))
        selected_cellar = get_user_default_cellar(user=request.user)

        for cellar in user_cellars:
            bottle = get_cellar_product_bottle(cellar=cellar, product=product)
            if bottle:
                product_bottles.append(bottle)

        cellar_id = request.GET.get("cellar_id")
        if cellar_id:
            selected_cellar = get_user_cellar_or_404(
                user=request.user,
                cellar_id=cellar_id,
            )

        if selected_cellar:
            bottle = get_cellar_product_bottle(cellar=selected_cellar, product=product)

    return render(
        request,
        "products/detail.html",
        {
            "product": product,
            "selected_cellar": selected_cellar,
            "cellars": user_cellars,
            "product_bottles": product_bottles,
        },
    )
