from django.urls import path
from products import views


app_name = "products"

urlpatterns = [
    path("", views.product_catalog, name="catalog"),
    path("<str:sku>/", views.product_detail, name="detail"),
]
