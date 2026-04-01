from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("signup/submit/", views.signup_submit, name="signup_submit"),
]
