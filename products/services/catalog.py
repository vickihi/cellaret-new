from dataclasses import dataclass

from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Count

from products.forms import (
    ProductCatalogSearchForm,
    ProductSortForm,
    ProductCatalogFilterForm,
)
from products.selectors import get_catalog_products
from products.models import Product


CATEGORY_PATH_LABELS = {
    "products/wine": "Wine",
    "products/spirit": "Spirit",
    "products/champagne-and-sparkling-wine": "Champagne & Sparkling Wine",
    "products/beer": "Beer",
    "products/cider": "Cider",
    "products/cooler-or-premixed-cocktail": "Cooler & Premixed Cocktail",
    "products/port-and-fortified-wine": "Port & Fortified Wine",
}


@dataclass
class CatalogPageData:
    form: ProductCatalogSearchForm
    sort_form: ProductSortForm
    filter_form: ProductCatalogFilterForm
    page_obj: object
    products: object
    search_query: str
    sort_key: str
    active_filters: dict
    available_filters: dict
    page_range: list
    breadcrumbs: list[dict[str, str | None]]


def get_available_filters(queryset=None):
    """Return available filters for catalog page and cellar page."""

    if queryset is None:
        queryset = Product.objects.all()

    category_paths = (
        queryset.exclude(category_path="")
        .values("category_path")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    categories = (
        queryset.exclude(category="")
        .values("category")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    countries = (
        queryset.exclude(country="")
        .values("country")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    taste_tags = (
        queryset.exclude(taste_tag="")
        .values("taste_tag")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    sizes = (
        queryset.exclude(size="")
        .values("size")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    categories_by_path = {}
    pairs = (
        queryset.exclude(category_path="")
        .exclude(category="")
        .values("category_path", "category")
        .distinct()
        .order_by("category_path", "category")
    )
    for row in pairs:
        categories_by_path.setdefault(row["category_path"], []).append(row["category"])

    return {
        "category_paths": [
            {
                "value": r["category_path"],
                "label": CATEGORY_PATH_LABELS.get(
                    r["category_path"], r["category_path"]
                ),
                "count": r["count"],
            }
            for r in category_paths
        ],
        "categories": [
            {"value": r["category"], "count": r["count"]} for r in categories
        ],
        "categories_by_path": categories_by_path,
        "countries": [{"value": r["country"], "count": r["count"]} for r in countries],
        "taste_tags": [
            {"value": r["taste_tag"], "count": r["count"]} for r in taste_tags
        ],
        "sizes": [{"value": r["size"], "count": r["count"]} for r in sizes],
    }


def build_catalog_page(*, data, page_number, per_page: int = 24) -> CatalogPageData:
    form = ProductCatalogSearchForm(data)
    sort_form = ProductSortForm(data)
    filter_form = ProductCatalogFilterForm(data)
    is_valid = form.is_valid()

    search_query = form.cleaned_data.get("q", "") if is_valid else ""
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

    products_qs = get_catalog_products(
        search_query=search_query, sort_key=sort_key, filters=filters
    )

    paginator = Paginator(products_qs, per_page)
    page_obj = paginator.get_page(page_number)
    elided_page_range = paginator.get_elided_page_range(
        page_obj.number, on_each_side=1, on_ends=1
    )  # type: ignore
    breadcrumbs = [
        {"label": "Catalog", "url": reverse("products:catalog")},
    ]
    if search_query:
        breadcrumbs.append(
            {
                "label": f"Search results for: {search_query}",
                "url": None,
            }
        )

    return CatalogPageData(
        form=form,
        sort_form=sort_form,
        filter_form=filter_form,
        page_obj=page_obj,
        products=page_obj.object_list,
        search_query=search_query,
        sort_key=sort_key,
        active_filters=filters,
        available_filters=get_available_filters(),
        page_range=elided_page_range,
        breadcrumbs=breadcrumbs,
    )
