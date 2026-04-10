from django.db.models import Case, IntegerField, Value, When, Q

from products.models import Product

SORT_TO_ORDER_BY = {
    "price_asc": ("price", "id"),
    "price_desc": ("-price", "id"),
    "name_asc": ("name", "id"),
    "name_desc": ("-name", "id"),
}


def apply_sort(qs, sort_key: str):
    if not sort_key:
        qs = qs.annotate(
            has_image=Case(
                When(image_url__isnull=False, image_url__gt="", then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        )
        return qs.order_by("-has_image", "name", "id")
    order_by_fields = SORT_TO_ORDER_BY.get(sort_key, ("name", "id"))
    return qs.order_by(*order_by_fields)


def apply_search(qs, search_query):
    if not search_query:
        return qs
    return qs.filter(
        Q(name__icontains=search_query)
        | Q(producer__icontains=search_query)
        | Q(region__icontains=search_query)
        | Q(country__icontains=search_query)
    )


def apply_filters(qs, filters: dict):
    """Apply selected filter values to the product queryset."""
    if filters.get("category_path"):
        qs = qs.filter(category_path__iexact=filters["category_path"])
    if filters.get("category"):
        qs = qs.filter(category__iexact=filters["category"])
    if filters.get("taste_tag"):
        qs = qs.filter(taste_tag__iexact=filters["taste_tag"])
    if filters.get("country"):
        qs = qs.filter(country__iexact=filters["country"])
    if filters.get("price_min") is not None:
        qs = qs.filter(price__gte=filters["price_min"])
    if filters.get("price_max") is not None:
        qs = qs.filter(price__lte=filters["price_max"])
    if filters.get("size"):
        qs = qs.filter(size__iexact=filters["size"])
    return qs


def get_catalog_products(
    *, search_query: str = "", sort_key: str = "", filters: dict | None = None
):
    qs = Product.objects.all()
    qs = apply_search(qs, search_query)
    qs = apply_filters(qs, filters or {})
    qs = apply_sort(qs, sort_key)
    return qs
