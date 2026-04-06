from cellars.models import Bottle, Cellar
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404


def get_user_cellars(*, user):
    """Get all cellars for a user."""
    cellars = user.cellars.annotate(
        bottle_count=Coalesce(Sum("bottles__quantity"), 0)
    ).order_by("id")
    return cellars


def get_user_cellar_or_404(*, user, cellar_id):
    """Get a cellar for a user."""
    return get_object_or_404(Cellar, id=cellar_id, user=user)


def get_cellar_bottles(*, cellar):
    """Get all bottles for a cellar."""
    return (
        Bottle.objects.filter(cellar=cellar)
        .select_related("product")
        .order_by("product__name", "id")
    )


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
