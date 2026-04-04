from django.urls import path
from cellars import views


app_name = "cellars"

urlpatterns = [
    path("", views.cellars, name="cellars"),
    path("create/", views.cellar_create, name="cellar_create"),
]
