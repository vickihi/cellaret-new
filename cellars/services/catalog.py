from dataclasses import dataclass

from django.core.paginator import Paginator
from django.db.models import Sum

from cellars.models import Bottle
from cellars.forms import CellarBottleSortForm
from cellars.selectors.cellars import apply_search, apply_sort
from products.forms import ProductCatalogFilterForm, ProductCatalogSearchForm
from products.models import Product
from products.selectors.product_catalog import apply_filters
from products.services.catalog import get_available_filters


@dataclass
class CellarPageData:
    form: ProductCatalogSearchForm
    filter_form: ProductCatalogFilterForm
    sort_form: CellarBottleSortForm
    page_obj: object
    bottles: object
    search_query: str
    sort_key: str
    active_filters: dict
    available_filters: dict
    page_range: list
    total_bottles: int


def build_cellar_page(*, cellar, data, page_number, per_page=24) -> CellarPageData:
    form = ProductCatalogSearchForm(data)
    filter_form = ProductCatalogFilterForm(data)
    sort_form = CellarBottleSortForm(data)
    search_query = form.cleaned_data.get("q", "") if form.is_valid() else ""
    sort_key = sort_form.cleaned_data.get("sort", "") if sort_form.is_valid() else ""

    filters = {}
    if filter_form.is_valid():
        cleaned = filter_form.cleaned_data
        for field in ["category_path", "category", "country", "taste_tag", "size"]:
            if cleaned.get(field):
                filters[field] = cleaned[field]
        if cleaned.get("price_min") is not None:
            filters["price_min"] = cleaned["price_min"]
        if cleaned.get("price_max") is not None:
            filters["price_max"] = cleaned["price_max"]

    cellar_products_qs = Product.objects.filter(bottles__cellar=cellar)
    filtered_cellar_products_qs = apply_filters(cellar_products_qs, filters)

    bottles_qs = Bottle.objects.filter(
        cellar=cellar, product__in=filtered_cellar_products_qs
    ).select_related("product")
    bottles_qs = apply_search(bottles_qs, search_query)
    bottles_qs = apply_sort(bottles_qs, sort_key)
    total_bottles = (
        Bottle.objects.filter(cellar=cellar).aggregate(total=Sum("quantity"))["total"]
        or 0
    )

    paginator = Paginator(bottles_qs, per_page)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(
        page_obj.number, on_each_side=1, on_ends=1
    )

    return CellarPageData(
        form=form,
        filter_form=filter_form,
        sort_form=sort_form,
        page_obj=page_obj,
        bottles=page_obj.object_list,
        search_query=search_query,
        sort_key=sort_key,
        active_filters=filters,
        available_filters=get_available_filters(cellar_products_qs),
        page_range=page_range,
        total_bottles=total_bottles,
    )
