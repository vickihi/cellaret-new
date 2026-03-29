from django.core.management.base import BaseCommand
from products.models import Product
from products.services.saq_api import fetch_all_products


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
        self.stdout.write("Fetching all products...")
        items = fetch_all_products()
        created, updated = self._save_products(items)
        self.stdout.write(self.style.SUCCESS(
            f"Done. Created: {created}, Updated: {updated}"
        ))

    def _save_products(self, items):
        created_count = 0
        updated_count = 0
        for item in items:
            _, created = Product.objects.update_or_create(
                sku=self._get_sku(item),
                defaults=self._build_defaults(item),
            )
            created_count += created
            updated_count += not created
        return created_count, updated_count

    def _build_defaults(self, item):
        product_view = item.get("productView") or {}
        attrs = {a["name"]: a["value"] for a in product_view.get("attributes", [])}
        return {
            "name":          product_view.get("name", ""),
            "description":   attrs.get("argumentaire_vente_externe", ""),
            "category":      attrs.get("identite_produit", ""),
            "image_url":     _get_image_url(product_view),
            "price":         _get_price(item),
            "grape_variety": _join_if_list(attrs.get("cepage")),
            "taste_tag":     _join_if_list(attrs.get("pastille_gout")),
            "country":       attrs.get("pays_origine", ""),
            "region":        attrs.get("region_origine", ""),
            "degree":        attrs.get("teneur_alcool", ""),
            "producer":      attrs.get("nom_producteur", ""),
            "size":          attrs.get("format_contenant_ml", ""),
            "vintage":       attrs.get("millesime_produit", ""),
        }

    def _get_sku(self, item):
        return (item.get("productView") or {}).get("sku")