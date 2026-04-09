from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from accounts.forms import (
    AccountProfileForm,
    LoginForm,
    SignUpForm,
    UsernameEmailPasswordResetForm,
)
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
    store_signup_redirect_target(request, request.GET.get("next"))

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
    messages.success(request, f"Welcome back, {user.username}!")

    return redirect(get_safe_redirect_target(request))


def logout(request):
    """Handle logout for user."""
    django_logout(request)

    return redirect("products:catalog")


@login_required
def detail(request):
    """Show account details for the current user."""
    cellars = request.user.cellars.all()

    return render(
        request,
        "accounts/detail.html",
        {
            "account_user": request.user,
            "profile_form": AccountProfileForm(instance=request.user),
            "cellars": cellars,
        },
    )


@login_required
def update_profile(request):
    """Update profile details for the current user."""
    if request.method != "POST":
        return redirect("accounts:detail")

    form = AccountProfileForm(request.POST, instance=request.user)
    if not form.is_valid():
        return render(
            request,
            "accounts/detail.html",
            {
                "account_user": request.user,
                "profile_form": form,
            },
        )

    form.save()
    messages.success(request, _("Your account details have been updated."))
    return redirect("accounts:detail")


class AccountPasswordChangeView(PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("accounts:detail")

    def form_valid(self, form):
        messages.success(
            request=self.request, message=_("Your password has been updated.")
        )
        return super().form_valid(form)


class AccountPasswordResetView(PasswordResetView):
    form_class = UsernameEmailPasswordResetForm
    template_name = "accounts/password_reset_form.html"
    email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")
