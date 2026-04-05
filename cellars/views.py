from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .selectors import (
    get_user_cellars,
    get_cellar_bottles,
    get_user_bottle_or_404,
    get_user_cellar_or_404,
)
from .services import create_cellar


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
def cellar_update(): ...


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
