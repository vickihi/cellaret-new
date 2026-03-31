from products.models import Product
from django.db.models import Case, IntegerField, Value, When

SORT_TO_ORDER_BY = {
    "price_asc": ("price", "id"),
    "price_desc": ("-price", "id"),
    "name_asc": ("name", "id"),
    "name_desc": ("-name", "id"),
}


def get_catalog_products(*, search_query: str = "", sort_key: str = ""):
    products = Product.objects.all()
    if search_query:
        products = products.filter(name__icontains=search_query)
    if sort_key == "":
        products = products.annotate(
            has_image=Case(
                When(image_url__isnull=False, image_url__gt="", then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        )
        return products.order_by("-has_image", "name", "id")
    order_by_fields = SORT_TO_ORDER_BY.get(sort_key, ("name", "id"))

    return products.order_by(*order_by_fields)
