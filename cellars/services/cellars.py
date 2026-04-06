from django.db import transaction

from cellars.models import Bottle, Cellar
from cellars.selectors import get_cellar_product_bottle


def _set_locked_bottle_quantity(*, bottle_id, quantity):
    """Persist a bottle quantity change and delete the row when empty."""
    bottle = Bottle.objects.select_for_update().get(id=bottle_id)

    if quantity <= 0:
        bottle.delete()
        return None

    bottle.quantity = quantity
    bottle.save(update_fields=["quantity"])
    return bottle


def create_cellar(*, name, description, user):    
    """Create a cellar for a user."""
    cellar = Cellar.objects.create(name=name, description=description, user=user)
    return cellar


def update_cellar(*, cellar, name, description):
    """Update a cellar for a user."""
    cellar.name = name
    cellar.description = description
    cellar.save()


def delete_cellar(*, cellar):
    """Delete a cellar for a user."""
    cellar.delete()


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
def add_product_to_cellar(*, cellar, product, quantity=1):
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
def decrease_product_quantity_in_cellar(*, cellar, product, quantity=1):
    """Decrease a product quantity in a cellar when the bottle entry exists."""
    bottle = get_cellar_product_bottle(cellar=cellar, product=product)
    if not bottle:
        return None

    return decrease_cellar_bottle_quantity(bottle=bottle, quantity=quantity)


@transaction.atomic
def set_product_quantity_in_cellar(*, cellar, product, quantity):
    """Set a product quantity in a cellar, creating the bottle entry when needed."""
    bottle = get_cellar_product_bottle(cellar=cellar, product=product)
    if bottle:
        return set_cellar_bottle_quantity(bottle=bottle, quantity=quantity)

    if quantity <= 0:
        return None

    return add_product_to_cellar(cellar=cellar, product=product, quantity=quantity)


@transaction.atomic
def decrease_cellar_bottle_quantity(*, bottle, quantity=1):
    """Decrease a cellar bottle quantity and delete the row when empty."""
    locked_bottle = Bottle.objects.select_for_update().get(id=bottle.id)
    next_quantity = locked_bottle.quantity - quantity
    return _set_locked_bottle_quantity(
        bottle_id=locked_bottle.id,
        quantity=next_quantity,
    )


@transaction.atomic
def set_cellar_bottle_quantity(*, bottle, quantity):
    """Set a cellar bottle quantity directly and delete the row when quantity is zero."""
    return _set_locked_bottle_quantity(bottle_id=bottle.id, quantity=quantity)


@transaction.atomic
def delete_cellar_bottle(*, bottle):
    """Delete a cellar bottle row."""
    return _set_locked_bottle_quantity(bottle_id=bottle.id, quantity=0)
