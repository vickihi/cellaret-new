from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product

from .forms import CellarForm

from .selectors import (
    get_cellar_bottle_or_404,
    get_cellar_product_bottle,
    get_user_cellars,
    get_user_cellar_or_404,
)

from .services import (
    create_cellar,
    update_cellar,
    delete_cellar,
    add_product_to_cellar,
    decrease_product_quantity_in_cellar,
    delete_cellar_bottle,
    get_or_create_default_cellar,
    set_product_quantity_in_cellar,
    set_cellar_bottle_quantity,
    build_cellar_page,
)


@login_required
def cellars(request):
    """
    Get all cellars for a user.
    If the user has no cellars, create one.
    """
    if not request.user.cellars.exists():
        create_cellar(
            name="Sample Cellar",
            description="This is a sample cellar ...",
            user=request.user,
        )

    cellars = get_user_cellars(user=request.user)
    return render(request, "cellars/cellars.html", {"cellars": cellars})


@login_required
def cellar_create(request):
    """Create a cellar for a user."""
    if request.method != "POST":
        return render(
            request,
            "cellars/cellar_create.html",
            {"form": CellarForm(user=request.user)},
        )

    form = CellarForm(request.POST, user=request.user)
    if not form.is_valid():
        return render(request, "cellars/cellar_create.html", {"form": form})

    create_cellar(
        name=form.cleaned_data["name"],
        description=form.cleaned_data["description"],
        user=request.user,
    )
    messages.success(request, "Your cellar has been created.")

    return redirect("cellars:cellars")


@login_required
@require_POST
def cellar_update(request, cellar_id):
    """Update a cellar for a user."""
    cellar = get_user_cellar_or_404(user=request.user, cellar_id=cellar_id)
    next_page = request.POST.get("next")
    form = CellarForm(request.POST, instance=cellar, user=request.user)

    if not form.is_valid():
        if next_page == "cellars":
            return redirect("cellars:cellar_detail", cellar_id=cellar_id)
        return redirect("accounts:detail")

    if form.has_changed():
        update_cellar(
            cellar=cellar,
            name=form.cleaned_data["name"],
            description=form.cleaned_data["description"],
        )
        messages.success(request, "Your cellar has been updated.")

    if next_page == "cellars":
        return redirect("cellars:cellar_detail", cellar_id=cellar_id)

    return redirect("accounts:detail")


@login_required
@require_POST
def cellar_delete(request, cellar_id):
    """Delete a cellar for a user."""
    cellar = get_user_cellar_or_404(user=request.user, cellar_id=cellar_id)
    delete_cellar(cellar=cellar)
    messages.success(request, f"Your cellar {cellar.name} has been deleted.")

    return redirect("accounts:detail")


@login_required
def cellar_detail(request, cellar_id):
    cellar = get_user_cellar_or_404(user=request.user, cellar_id=cellar_id)
    cellars = get_user_cellars(user=request.user)

    cellar_page = build_cellar_page(
        cellar=cellar,
        data=request.GET,
        page_number=request.GET.get("page", 1),
    )

    return render(
        request,
        "cellars/cellar_detail.html",
        {
            "cellars": cellars,
            "cellar": cellar,
            "bottles": cellar_page.bottles,
            "sort_form": cellar_page.sort_form,
            "filter_form": cellar_page.filter_form,
            "page_obj": cellar_page.page_obj,
            "page_range": cellar_page.page_range,
            "sort_key": cellar_page.sort_key,
            "active_filters": cellar_page.active_filters,
            "available_filters": cellar_page.available_filters,
            "total_bottles": cellar_page.total_bottles,
        },
    )


def _redirect_to_next_or_cellar_detail(request, *, cellar_id):
    redirect_to = request.POST.get("next")
    if redirect_to:
        return redirect(redirect_to)

    return redirect("cellars:cellar_detail", cellar_id=cellar_id)


def _get_requested_or_default_user_cellar(*, request):
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
    add_product_to_cellar(cellar=cellar, product=product)
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
    cellar = _get_requested_or_default_user_cellar(request=request)
    add_product_to_cellar(cellar=cellar, product=product)
    messages.success(request, f"Added {product.name} to {cellar.name}.")

    redirect_to = request.POST.get("next")
    if redirect_to:
        return redirect(redirect_to)

    return redirect("products:detail", sku=sku)


@login_required
def bottle_remove(request, sku):
    if request.method != "POST":
        return redirect("products:detail", sku=sku)

    product = get_object_or_404(Product, sku=sku)
    cellar = _get_requested_or_default_user_cellar(request=request)
    if cellar:
        decrease_product_quantity_in_cellar(cellar=cellar, product=product)
        messages.success(request, f"Removed {product.name} from {cellar.name}.")

    redirect_to = request.POST.get("next")
    if redirect_to:
        return redirect(redirect_to)

    return redirect("products:detail", sku=sku)


@login_required
def bottle_set_quantity(request, sku):
    if request.method != "POST":
        return redirect("products:detail", sku=sku)

    product = get_object_or_404(Product, sku=sku)
    cellar = _get_requested_or_default_user_cellar(request=request)

    try:
        quantity = int(request.POST.get("quantity", 0))
    except (TypeError, ValueError):
        current_bottle = get_cellar_product_bottle(cellar=cellar, product=product)
        quantity = current_bottle.quantity if current_bottle else 0

    set_product_quantity_in_cellar(cellar=cellar, product=product, quantity=quantity)

    redirect_to = request.POST.get("next")
    if redirect_to:
        return redirect(redirect_to)

    return redirect("products:detail", sku=sku)


@login_required
def cellar_bottle_delete(request, cellar_id, bottle_id):
    if request.method != "POST":
        return redirect("cellars:cellar_detail", cellar_id=cellar_id)

    cellar = get_user_cellar_or_404(user=request.user, cellar_id=cellar_id)
    bottle = get_cellar_bottle_or_404(cellar=cellar, bottle_id=bottle_id)
    delete_cellar_bottle(bottle=bottle)
    messages.success(request, f"Removed {bottle.product.name} from {cellar.name}.")

    return _redirect_to_next_or_cellar_detail(request, cellar_id=cellar_id)


@login_required
def cellar_bottle_save(request, cellar_id, bottle_id):
    if request.method != "POST":
        return redirect("cellars:cellar_detail", cellar_id=cellar_id)

    cellar = get_user_cellar_or_404(user=request.user, cellar_id=cellar_id)
    bottle = get_cellar_bottle_or_404(cellar=cellar, bottle_id=bottle_id)

    try:
        quantity = int(request.POST.get("quantity", bottle.quantity))
    except (TypeError, ValueError):
        quantity = bottle.quantity

    set_cellar_bottle_quantity(bottle=bottle, quantity=quantity)
    messages.success(
        request, f"Updated {bottle.product.name} quantity in {cellar.name}."
    )

    return _redirect_to_next_or_cellar_detail(request, cellar_id=cellar_id)
