from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product

from .selectors import (
    get_cellar_product_bottle,
    get_user_cellars,
    get_cellar_bottles,
    get_user_bottle_or_404,
    get_user_cellar_or_404,
)
from .services import (
    add_bottle_to_cellar,
    create_cellar,
    get_or_create_default_cellar,
    remove_bottle_from_cellar,
    set_bottle_quantity,
)


@login_required
def cellars(request):
    """
    Get all cellars for a user.
    If the user has no cellars, create one.
    """
    if not request.user.cellars.exists():
        create_cellar(
            name="My Cellar",
            description="This is my first cellar ...",
            user=request.user,
        )

    cellars = get_user_cellars(user=request.user)
    return render(request, "cellars/cellars.html", {"cellars": cellars})


@login_required
def cellar_create(request):
    """Create a cellar for a user."""
    if request.method == "POST":
        create_cellar(
            name=request.POST["name"],
            description=request.POST["description"],
            user=request.user,
        )
        return redirect("cellars:cellars")

    return render(request, "cellars/cellar_create.html")


@login_required
def cellar_detail(request, cellar_id):
    cellar = get_user_cellar_or_404(user=request.user, cellar_id=cellar_id)
    bottles = get_cellar_bottles(cellar=cellar)
    return render(
        request,
        "cellars/cellar_detail.html",
        {
            "cellar": cellar,
            "bottles": bottles,
        },
    )


def _redirect_to_cellar_bottle_next(request, *, cellar_id):
    redirect_to = request.POST.get("next")
    if redirect_to:
        return redirect(redirect_to)

    return redirect("cellars:cellar_detail", cellar_id=cellar_id)


def _get_requested_or_default_cellar(*, request):
    cellar_id = request.POST.get("cellar_id")
    if cellar_id:
        return get_user_cellar_or_404(user=request.user, cellar_id=cellar_id)

    return get_or_create_default_cellar(user=request.user)


@login_required
def cellar_bottle_add(request, cellar_id, sku):
    cellar = get_user_cellar_or_404(user=request.user, cellar_id=cellar_id)
    if request.method != "POST":
        return redirect("products:catalog")

    product = get_object_or_404(Product, sku=sku)
    add_bottle_to_cellar(cellar=cellar, product=product)
    messages.success(request, f"Added {product.name} to {cellar.name}.")

    redirect_to = request.POST.get("next")
    if redirect_to:
        return redirect(redirect_to)

    return redirect("cellars:cellar_detail", cellar_id=cellar.id)


@login_required
def bottle_add(request, sku):
    if request.method != "POST":
        return redirect("products:detail", sku=sku)

    product = get_object_or_404(Product, sku=sku)
    cellar = _get_requested_or_default_cellar(request=request)
    add_bottle_to_cellar(cellar=cellar, product=product)

    redirect_to = request.POST.get("next")
    if redirect_to:
        return redirect(redirect_to)

    return redirect("products:detail", sku=sku)


@login_required
def bottle_remove(request, sku):
    if request.method != "POST":
        return redirect("products:detail", sku=sku)

    product = get_object_or_404(Product, sku=sku)
    cellar = _get_requested_or_default_cellar(request=request)
    if cellar:
        bottle = get_cellar_product_bottle(cellar=cellar, product=product)
        if bottle:
            remove_bottle_from_cellar(bottle=bottle)

    redirect_to = request.POST.get("next")
    if redirect_to:
        return redirect(redirect_to)

    return redirect("products:detail", sku=sku)


@login_required
def bottle_set_quantity(request, sku):
    if request.method != "POST":
        return redirect("products:detail", sku=sku)

    product = get_object_or_404(Product, sku=sku)
    cellar = _get_requested_or_default_cellar(request=request)
    bottle = get_cellar_product_bottle(cellar=cellar, product=product)

    try:
        quantity = int(request.POST.get("quantity", 0))
    except (TypeError, ValueError):
        quantity = bottle.quantity if bottle else 0

    if bottle:
        set_bottle_quantity(bottle=bottle, quantity=quantity)
    elif quantity > 0:
        add_bottle_to_cellar(cellar=cellar, product=product, quantity=quantity)

    redirect_to = request.POST.get("next")
    if redirect_to:
        return redirect(redirect_to)

    return redirect("products:detail", sku=sku)


@login_required
def cellar_bottle_remove(request, cellar_id, bottle_id):
    if request.method != "POST":
        return redirect("cellars:cellar_detail", cellar_id=cellar_id)

    cellar = get_user_cellar_or_404(user=request.user, cellar_id=cellar_id)
    bottle = get_user_bottle_or_404(cellar=cellar, bottle_id=bottle_id)
    remove_bottle_from_cellar(bottle=bottle)

    return redirect("cellars:cellar_detail", cellar_id=cellar_id)


@login_required
def cellar_bottle_increase(request, cellar_id, bottle_id):
    if request.method != "POST":
        return redirect("cellars:cellar_detail", cellar_id=cellar_id)

    cellar = get_user_cellar_or_404(user=request.user, cellar_id=cellar_id)
    bottle = get_user_bottle_or_404(cellar=cellar, bottle_id=bottle_id)
    add_bottle_to_cellar(cellar=cellar, product=bottle.product)

    return _redirect_to_cellar_bottle_next(request, cellar_id=cellar_id)


@login_required
def cellar_bottle_decrease(request, cellar_id, bottle_id):
    if request.method != "POST":
        return redirect("cellars:cellar_detail", cellar_id=cellar_id)

    cellar = get_user_cellar_or_404(user=request.user, cellar_id=cellar_id)
    bottle = get_user_bottle_or_404(cellar=cellar, bottle_id=bottle_id)
    remove_bottle_from_cellar(bottle=bottle)

    return _redirect_to_cellar_bottle_next(request, cellar_id=cellar_id)


@login_required
def cellar_bottle_delete(request, cellar_id, bottle_id):
    if request.method != "POST":
        return redirect("cellars:cellar_detail", cellar_id=cellar_id)

    cellar = get_user_cellar_or_404(user=request.user, cellar_id=cellar_id)
    bottle = get_user_bottle_or_404(cellar=cellar, bottle_id=bottle_id)
    set_bottle_quantity(bottle=bottle, quantity=0)

    return _redirect_to_cellar_bottle_next(request, cellar_id=cellar_id)


@login_required
def cellar_bottle_save(request, cellar_id, bottle_id):
    if request.method != "POST":
        return redirect("cellars:cellar_detail", cellar_id=cellar_id)

    cellar = get_user_cellar_or_404(user=request.user, cellar_id=cellar_id)
    bottle = get_user_bottle_or_404(cellar=cellar, bottle_id=bottle_id)

    try:
        quantity = int(request.POST.get("quantity", bottle.quantity))
    except (TypeError, ValueError):
        quantity = bottle.quantity

    set_bottle_quantity(bottle=bottle, quantity=quantity)

    return _redirect_to_cellar_bottle_next(request, cellar_id=cellar_id)


@login_required
def single_bottle(request, cellar_id, bottle_id):
    cellar = get_user_cellar_or_404(user=request.user, cellar_id=cellar_id)
    bottle = get_user_bottle_or_404(cellar=cellar, bottle_id=bottle_id)

    return render(
        request,
        "cellars/single_bottle.html",
        {
            "cellar": cellar,
            "bottle": bottle,
            "product": bottle.product,
        },
    )
