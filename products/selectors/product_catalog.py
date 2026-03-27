from products.models import Product


def get_catalog_products(*, search_query: str = ""):
    products = Product.objects.order_by("name", "id")

    if search_query:
        products = products.filter(name__icontains=search_query)

    return products
