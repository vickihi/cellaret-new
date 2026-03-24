from django.urls import path

from .views import product_catalog

app_name = "products"

urlpatterns = [
    path("", product_catalog, name="catalog"),
]
