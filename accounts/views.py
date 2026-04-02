from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from accounts.forms import SignUpForm, LoginForm
from accounts.services.auth_service import (
    create_user_account,
)
from accounts.utils import get_safe_redirect_target, store_signup_redirect_target


def signup(request):
    if request.user.is_authenticated:
        return redirect("products:catalog")

    store_signup_redirect_target(request, request.GET.get("next"))
    context = {
        "form": SignUpForm(),
    }
    return render(request, "accounts/signup.html", context)


def signup_submit(request):
    if request.user.is_authenticated:
        return redirect("products:catalog")

    if request.method == "POST":
        store_signup_redirect_target(request, request.POST.get("next"))
    else:
        store_signup_redirect_target(request, request.GET.get("next"))

    form = SignUpForm(request.POST or None)

    if request.method != "POST" or not form.is_valid():
        return render(
            request,
            "accounts/signup.html",
            {
                "form": form,
            },
        )

    user = create_user_account(
        username=form.cleaned_data["username"],
        email=form.cleaned_data.get("email", ""),
        password=form.cleaned_data["password1"],
    )
    django_login(request, user)
    messages.success(
        request, _("Your account has been created and you are now signed in.")
    )
    return redirect(get_safe_redirect_target(request))


def login(request):
    """Show form for log in."""
    if request.user.is_authenticated:
        return redirect(get_safe_redirect_target(request))

    form = LoginForm(request)
    context = {"form": form}

    return render(request, "accounts/login.html", context)


def login_submit(request):
    """Handle form for log in."""
    form = LoginForm(request, data=request.POST)
    context = {"form": form}

    if not form.is_valid():
        return render(request, "accounts/login.html", context)

    user = form.get_user()
    django_login(request, user)

    return redirect(get_safe_redirect_target(request))


def logout(request):
    """Handle logout for user."""
    store_signup_redirect_target(request, request.POST.get("next"))
    django_logout(request)
    return redirect(get_safe_redirect_target(request))
