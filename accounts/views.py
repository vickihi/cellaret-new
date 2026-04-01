from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from accounts.forms import SignUpForm
from accounts.services.auth_service import (
    create_user_account,
)
from accounts.utils import get_safe_redirect_target


def signup(request):
    if request.user.is_authenticated:
        return redirect("products:catalog")

    context = {
        "form": SignUpForm(),
        "next": request.GET.get("next", ""),
    }
    return render(request, "accounts/signup.html", context)


def signup_submit(request):
    if request.user.is_authenticated:
        return redirect("products:catalog")

    form = SignUpForm(request.POST or None)

    if request.method != "POST" or not form.is_valid():
        return render(
            request,
            "accounts/signup.html",
            {
                "form": form,
                "next": request.POST.get("next", request.GET.get("next", "")),
            },
        )

    user = create_user_account(
        username=form.cleaned_data["username"],
        email=form.cleaned_data.get("email", ""),
        password=form.cleaned_data["password1"],
    )
    login(request, user)
    messages.success(
        request, _("Your account has been created and you are now signed in.")
    )
    return redirect(get_safe_redirect_target(request))
