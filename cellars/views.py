from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .selectors import get_user_cellars
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
