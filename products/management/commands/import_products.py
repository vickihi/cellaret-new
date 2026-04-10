from django.core.management.base import BaseCommand
from products.models import Product
from products.services.saq_api import fetch_all_products, fetch_products_by_filter, CATALOG_TYPE_1_PRICE_RANGES


CATEGORY_PATHS = [
    "products/wine",
    "products/spirit",
    "products/champagne-and-sparkling-wine",
    "products/beer",
    "products/cider",
    "products/cooler-or-premixed-cocktail",
    "products/port-and-fortified-wine",
]


def _get_price(item):
    try:
        return item["product"]["price_range"]["minimum_price"]["regular_price"]["value"]
    except (KeyError, TypeError):
        return None


def _join_if_list(value):
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return value or ""


def _get_image_url(product_view):
    images = product_view.get("images") or []
    if not images:
        return ""
    return (images[0] or {}).get("url") or ""


class Command(BaseCommand):
    help = "Import products from SAQ API into Product model"

    def handle(self, *args, **options):
        self.stdout.write("Building SKU → category map...")
        sku_category_map = self._build_sku_category_map()
        self.stdout.write(f"Mapped {len(sku_category_map)} SKUs to categories.")

        self.stdout.write("Fetching all products...")
        items = fetch_all_products()

        items_dict = {}
        for item in items:
            sku = self._get_sku(item)
            if sku:
                items_dict[sku] = item

        self.stdout.write(f"Processing {len(items_dict)} unique products...")

        existing_skus = set(Product.objects.values_list("sku", flat=True))

        to_create = []
        to_update = []

        for sku, item in items_dict.items():
            if sku in existing_skus:
                to_update.append((sku, item))
            else:
                to_create.append(self._build_product(item, sku, sku_category_map))

        if to_create:
            self.stdout.write(f"Creating {len(to_create)} products...")
            Product.objects.bulk_create(to_create, batch_size=500)

        updated_count = 0
        if to_update:
            self.stdout.write(f"Updating {len(to_update)} products...")
            for i in range(0, len(to_update), 500):
                batch = to_update[i : i + 500]
                skus = [sku for sku, _ in batch]

                products = {p.sku: p for p in Product.objects.filter(sku__in=skus)}

                for sku, item in batch:
                    if sku in products:
                        self._update_product(products[sku], item, sku_category_map)

                Product.objects.bulk_update(
                    products.values(),
                    [
                        "name",
                        "description",
                        "category",
                        "category_path",
                        "image_url",
                        "price",
                        "grape_variety",
                        "taste_tag",
                        "country",
                        "region",
                        "degree",
                        "producer",
                        "size",
                        "vintage",
                    ],
                    batch_size=500,
                )
                updated_count += len(batch)

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created: {len(to_create)}, Updated: {updated_count}"
            )
        )

    def _build_sku_category_map(self):
        sku_map = {}
        for path in CATEGORY_PATHS:
            self.stdout.write(f"  Fetching category: {path}...")
            for price_from, price_to in CATALOG_TYPE_1_PRICE_RANGES:
                page = 1
                while True:
                    result = fetch_products_by_filter(
                        page=page,
                        page_size=500,
                        filters=[
                            {"attribute": "categories", "eq": path},
                            {"attribute": "catalog_type", "eq": "1"},
                            {"attribute": "price", "range": {"from": price_from, "to": price_to}},
                        ],
                    )
                    items = result.get("items", [])
                    for item in items:
                        sku = self._get_sku(item)
                        if sku and sku not in sku_map:
                            sku_map[sku] = path
                    if len(items) < 500:
                        break
                    page += 1
            page = 1
            while True:
                result = fetch_products_by_filter(
                    page=page,
                    page_size=500,
                    filters=[
                        {"attribute": "categories", "eq": path},
                        {"attribute": "catalog_type", "eq": "2"},
                    ],
                )
                items = result.get("items", [])
                for item in items:
                    sku = self._get_sku(item)
                    if sku and sku not in sku_map:
                        sku_map[sku] = path
                if len(items) < 500:
                    break
                page += 1
        return sku_map

    def _build_product(self, item, sku, sku_category_map):
        product_view = item.get("productView") or {}
        attrs = {a["name"]: a["value"] for a in product_view.get("attributes", [])}

        return Product(
            sku=sku,
            name=product_view.get("name", ""),
            description=attrs.get("argumentaire_vente_externe", ""),
            category=attrs.get("identite_produit", ""),
            category_path=sku_category_map.get(sku, ""),
            image_url=_get_image_url(product_view),
            price=_get_price(item),
            grape_variety=_join_if_list(attrs.get("cepage")),
            taste_tag=_join_if_list(attrs.get("pastille_gout")),
            country=attrs.get("pays_origine", ""),
            region=attrs.get("region_origine", ""),
            degree=attrs.get("teneur_alcool", ""),
            producer=attrs.get("nom_producteur", ""),
            size=attrs.get("format_contenant_ml", ""),
            vintage=attrs.get("millesime_produit", ""),
        )

    def _update_product(self, product, item, sku_category_map):
        product_view = item.get("productView") or {}
        attrs = {a["name"]: a["value"] for a in product_view.get("attributes", [])}

        product.name = product_view.get("name", "")
        product.description = attrs.get("argumentaire_vente_externe", "")
        product.category = attrs.get("identite_produit", "")
        product.category_path = sku_category_map.get(product.sku, "")
        product.image_url = _get_image_url(product_view)
        product.price = _get_price(item)
        product.grape_variety = _join_if_list(attrs.get("cepage"))
        product.taste_tag = _join_if_list(attrs.get("pastille_gout"))
        product.country = attrs.get("pays_origine", "")
        product.region = attrs.get("region_origine", "")
        product.degree = attrs.get("teneur_alcool", "")
        product.producer = attrs.get("nom_producteur", "")
        product.size = attrs.get("format_contenant_ml", "")
        product.vintage = attrs.get("millesime_produit", "")

    def _get_sku(self, item):
        return (item.get("productView") or {}).get("sku")
