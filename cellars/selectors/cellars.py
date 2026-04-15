from cellars.models import Bottle, Cellar
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404

SORT_TO_ORDER_BY = {
    "price_asc": ("product__price", "id"),
    "price_desc": ("-product__price", "id"),
    "name_asc": ("product__name", "id"),
    "name_desc": ("-product__name", "id"),
    "quantity_desc": ("-quantity", "id"),
    "quantity_asc": ("quantity", "id"),
}


def apply_sort(qs, sort_key: str):
    """Reuse sort function for cellars"""
    order_by_fields = SORT_TO_ORDER_BY.get(sort_key, ("product__name", "id"))
    return qs.order_by(*order_by_fields)

def apply_search(qs, search_query:str):
    if not search_query:
        return qs
    return qs.filter(
        Q(product__name__icontains=search_query)
    )

def get_user_cellars(*, user):
    """Get all cellars for a user."""
    cellars = user.cellars.annotate(
        bottle_count=Coalesce(Sum("bottles__quantity"), 0)
    ).order_by("id")
    return cellars


def get_user_cellar_or_404(*, user, cellar_id):
    """Get a cellar for a user."""
    return get_object_or_404(Cellar, id=cellar_id, user=user)


def get_cellar_bottles(*, cellar, sort_key: str = ""):
    """Get all bottles for a cellar."""
    qs = Bottle.objects.filter(cellar=cellar).select_related("product")
    return apply_sort(qs, sort_key)


def get_cellar_bottle_or_404(*, cellar, bottle_id):
    """Get a bottle for a cellar."""
    return get_object_or_404(
        Bottle.objects.select_related("product"),
        id=bottle_id,
        cellar=cellar,
    )


def get_user_default_cellar(*, user):
    """Get the first cellar for a user."""
    return user.cellars.order_by("id").first()


def get_cellar_product_bottle(*, cellar, product):
    """Get the bottle entry for a product inside a cellar."""
    return (
        Bottle.objects.select_related("product")
        .filter(cellar=cellar, product=product)
        .first()
    )
