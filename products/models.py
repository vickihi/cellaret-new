from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    taste_tag = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    degree = models.CharField(max_length=50, blank=True)
    producer = models.CharField(max_length=200, blank=True)
    size = models.CharField(max_length=50, blank=True)
    vintage = models.CharField(max_length=20, blank=True)
    grape_variety = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"
