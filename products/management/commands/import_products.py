from django.core.management.base import BaseCommand
from products.models import Product
from products.services.saq_api import fetch_products


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
        self.stdout.write("Fetching products from SAQ API...")

        # Testing: fetch first 20 products
        data = fetch_products(page=1, page_size=20)
        all_products = data["items"]

        # Production: fetch all products
        # all_products = fetch_products_pages(max_pages=200)

        self.stdout.write(f"Total products fetched: {len(all_products)}")

        created_count = 0
        updated_count = 0

        for item in all_products:
            product_view = item.get("productView") or {}
            attrs = {
                attr["name"]: attr["value"]
                for attr in product_view.get("attributes", [])
            }

            _, created = Product.objects.update_or_create(
                sku=product_view["sku"],
                defaults={
                    "name": product_view.get("name", ""),
                    "description": attrs.get("argumentaire_vente_externe", ""),
                    "category": attrs.get("identite_produit", ""),
                    "image_url": _get_image_url(product_view),
                    "price": _get_price(item),
                    "grape_variety": _join_if_list(attrs.get("cepage")),
                    "taste_tag": _join_if_list(attrs.get("pastille_gout")),
                    "country": attrs.get("pays_origine", ""),
                    "region": attrs.get("region_origine", ""),
                    "degree": attrs.get("teneur_alcool", ""),
                    "producer": attrs.get("nom_producteur", ""),
                    "size": attrs.get("format_contenant_ml", ""),
                    "vintage": attrs.get("millesime_produit", ""),
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created: {created_count}, Updated: {updated_count}"
            )
        )
