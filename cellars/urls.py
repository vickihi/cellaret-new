from django.urls import path
from cellars import views


app_name = "cellars"

urlpatterns = [
    path("", views.cellars, name="cellars"),
    path("create/", views.cellar_create, name="cellar_create"),
    path("bottles/<str:sku>/add/", views.bottle_add, name="bottle_add"),
    path("bottles/<str:sku>/remove/", views.bottle_remove, name="bottle_remove"),
    path("<int:cellar_id>/", views.cellar_detail, name="cellar_detail"),
    path(
        "<int:cellar_id>/bottles/<int:bottle_id>/remove/",
        views.cellar_bottle_remove,
        name="cellar_bottle_remove",
    ),
    path(
        "<int:cellar_id>/bottles/<int:bottle_id>/",
        views.single_bottle,
        name="single_bottle",
    ),
]
