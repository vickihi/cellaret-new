from cellars.models import Bottle, Cellar
from django.shortcuts import get_object_or_404


def get_user_cellars(*, user):
    """Get all cellars for a user."""
    cellars = user.cellars.all()
    return cellars


def get_user_cellar_or_404(*, user, cellar_id):
    """Get a cellar for a user."""
    return get_object_or_404(Cellar, id=cellar_id, user=user)


def get_cellar_bottles(*, cellar):
    """Get all bottles for a cellar."""
    return Bottle.objects.filter(cellar=cellar).select_related("product")


def get_user_bottle_or_404(*, cellar, bottle_id):
    """Get a bottle for a cellar."""
    return get_object_or_404(
        Bottle.objects.select_related("product"),
        id=bottle_id,
        cellar=cellar,
    )
