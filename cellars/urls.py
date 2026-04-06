from django.urls import path
from cellars import views


app_name = "cellars"

urlpatterns = [
    path("", views.cellars, name="cellars"),
    path("create/", views.cellar_create, name="cellar_create"),
    path("bottles/<str:sku>/add/", views.bottle_add, name="bottle_add"),
    path("bottles/<str:sku>/remove/", views.bottle_remove, name="bottle_remove"),
    path(
        "bottles/<str:sku>/set-quantity/",
        views.bottle_set_quantity,
        name="bottle_set_quantity",
    ),
    path("<int:cellar_id>/", views.cellar_detail, name="cellar_detail"),
    path(
        "<int:cellar_id>/bottles/add/<str:sku>/",
        views.cellar_bottle_add,
        name="cellar_bottle_add",
    ),
    path(
        "<int:cellar_id>/bottles/<int:bottle_id>/delete/",
        views.cellar_bottle_delete,
        name="cellar_bottle_delete",
    ),
    path(
        "<int:cellar_id>/bottles/<int:bottle_id>/save/",
        views.cellar_bottle_save,
        name="cellar_bottle_save",
    ),
]
