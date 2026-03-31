from products.models import Product

SORT_TO_ORDER_BY = {
    "default": ("name", "id"),
    "price_asc": ("price", "id"),
    "price_desc": ("-price", "id"),
    "name_asc": ("name", "id"),
    "name_desc": ("-name", "id"),
}


def get_catalog_products(*, search_query: str = "", sort_key: str = "default"):
    products = Product.objects.all()
    if search_query:
        products = products.filter(name__icontains=search_query)

    order_by_fields = SORT_TO_ORDER_BY.get(sort_key, SORT_TO_ORDER_BY["default"])

    return products.order_by(*order_by_fields)
