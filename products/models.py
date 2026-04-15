from decimal import Decimal, InvalidOperation

from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    category_path = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    taste_tag = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    degree = models.CharField(max_length=50, blank=True)
    producer = models.CharField(max_length=200, blank=True)
    size = models.CharField(max_length=50, blank=True)
    vintage = models.CharField(max_length=20, blank=True)
    grape_variety = models.CharField(max_length=500, blank=True)

    @property
    def size_display(self):
        """Return the product size formatted as mL below 1000 and L at 1000 or above."""
        if not self.size:
            return ""

        try:
            ml = float(self.size)
        except (TypeError, ValueError):
            return self.size

        if ml < 1000:
            return f"{int(ml)} ml" if ml.is_integer() else f"{ml:g} ml"

        liters = ml / 1000
        return f"{liters:g} L"

    @property
    def degree_display(self):
        """Return alcohol degree formatted for display."""
        if not self.degree:
            return ""

        degree = str(self.degree).strip()
        if not degree:
            return ""

        if "%" in degree:
            return degree

        try:
            numeric_degree = Decimal(degree)
        except (InvalidOperation, TypeError, ValueError):
            return degree

        return f"{numeric_degree.normalize():f}".rstrip("0").rstrip(".") + "%"

    def __str__(self):
        return f"{self.name} ({self.sku})"
