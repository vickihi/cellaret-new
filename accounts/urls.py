from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from accounts import views

app_name = "accounts"

urlpatterns = [
    path("", views.detail, name="detail"),
    path("profile/", views.update_profile, name="update_profile"),
    path(
        "password/", views.AccountPasswordChangeView.as_view(), name="change_password"
    ),
    path(
        "password-reset/",
        views.AccountPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path("signup/", views.signup, name="signup"),
    path("signup/submit/", views.signup_submit, name="signup_submit"),
    path("login/", views.login, name="login"),
    path("login/submit/", views.login_submit, name="login_submit"),
    path("logout/", views.logout, name="logout"),
]
