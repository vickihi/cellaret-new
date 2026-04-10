from django import forms
from django.db.models import Count
from products.models import Product


class ProductCatalogSearchForm(forms.Form):
    q = forms.CharField(
        label="Search products",
        max_length=200,
        required=False,
        strip=True,
    )


class ProductSortForm(forms.Form):
    SORT = [
        ("", "Default"),
        ("name_asc", "Name (A-Z)"),
        ("name_desc", "Name (Z-A)"),
        ("price_asc", "Price (low to high)"),
        ("price_desc", "Price (high to low)"),
    ]

    sort = forms.ChoiceField(
        label="Sort:",
        required=False,
        choices=SORT,
        initial="",
        widget=forms.Select(attrs={"class": "sort-select"}),
    )


class ProductCatalogFilterForm(forms.Form):
    """Form for catalog filters."""

    category_path = forms.ChoiceField(required=False, choices=[("", "All Categories")])
    category = forms.ChoiceField(required=False, choices=[("", "Categories")])
    country = forms.ChoiceField(required=False, choices=[("", "Countries")])
    taste_tag = forms.ChoiceField(required=False, choices=[("", "Taste tags")])
    size = forms.ChoiceField(required=False, choices=[("", "Sizes")])
    price_min = forms.DecimalField(
        required=False, max_digits=8, decimal_places=2, label="Minimum Price"
    )
    price_max = forms.DecimalField(
        required=False, max_digits=8, decimal_places=2, label="Maximum Price"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category_path"].choices += self._distinct_choices_by_count(
            "category_path"
        )
        self.fields["category"].choices += self._distinct_choices_by_count("category")
        self.fields["taste_tag"].choices += self._distinct_choices_by_count("taste_tag")
        self.fields["country"].choices += self._distinct_choices_by_count("country")
        self.fields["size"].choices += self._distinct_choices_by_count("size")

    @staticmethod
    def _distinct_choices_by_count(field_name: str):
        """Return non-empty distinct values ordered by usage count."""
        rows = (
            Product.objects.exclude(**{field_name: ""})
            .exclude(**{field_name: None})
            .values(field_name)
            .annotate(total=Count("id"))
            .distinct()
            .order_by("-total", field_name)
        )

        return [(row[field_name], row[field_name]) for row in rows if row[field_name]]

    def clean(self):
        cleaned = super().clean()
        min_price = cleaned.get("price_min")
        max_price = cleaned.get("price_max")
        if min_price is not None and max_price is not None:
            if min_price > max_price:
                raise forms.ValidationError(
                    "Max price must be greater than or equal to min price."
                )
        return cleaned
