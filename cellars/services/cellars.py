from django.db import transaction

from cellars.models import Bottle, Cellar


def create_cellar(*, name, description, user):
    """Create a cellar for a user."""
    cellar = Cellar.objects.create(name=name, description=description, user=user)

    return cellar


def get_or_create_default_cellar(*, user):
    """Get a user's first cellar or create a default one."""
    cellar = user.cellars.order_by("id").first()
    if cellar:
        return cellar

    return create_cellar(
        name="My Cellar",
        description="This is my first cellar ...",
        user=user,
    )


@transaction.atomic
def add_bottle_to_cellar(*, cellar, product, quantity=1):
    """Add a product to a cellar and increase quantity when it already exists."""
    bottle, created = Bottle.objects.select_for_update().get_or_create(
        cellar=cellar,
        product=product,
        defaults={"quantity": quantity},
    )

    if not created:
        bottle.quantity += quantity
        bottle.save(update_fields=["quantity"])

    return bottle


@transaction.atomic
def remove_bottle_from_cellar(*, bottle, quantity=1):
    """Remove bottles from a cellar entry and delete it when empty."""
    bottle = Bottle.objects.select_for_update().get(id=bottle.id)

    if bottle.quantity <= quantity:
        bottle.delete()
        return None

    bottle.quantity -= quantity
    bottle.save(update_fields=["quantity"])
    return bottle
