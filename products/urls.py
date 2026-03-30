from django.urls import path
from .views import product_catalog, product_detail


app_name = "products"

urlpatterns = [
    path("", product_catalog, name="catalog"),
    path("<str:sku>/", product_detail, name="detail"),
]
