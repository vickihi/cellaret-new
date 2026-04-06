from django.conf import settings
from django.db import models

from products.models import Product


class Cellar(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="cellars", on_delete=models.CASCADE
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "user"], name="unique_cellar_name_per_user"
            )
        ]

    def __str__(self):
        return self.name

class Bottle(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(
        Product, related_name="bottles", on_delete=models.CASCADE
    )
    cellar = models.ForeignKey(Cellar, related_name="bottles", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cellar", "product"], name="unique_product_per_cellar"
            )
        ]
