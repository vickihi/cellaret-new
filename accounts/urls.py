from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path("", views.detail, name="detail"),
    path("profile/", views.update_profile, name="update_profile"),
    path(
        "password/", views.AccountPasswordChangeView.as_view(), name="change_password"
    ),
    path("signup/", views.signup, name="signup"),
    path("signup/submit/", views.signup_submit, name="signup_submit"),
    path("login/", views.login, name="login"),
    path("login/submit/", views.login_submit, name="login_submit"),
    path("logout/", views.logout, name="logout"),
]
