from django import forms

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
    category = forms.ChoiceField(required=False, choices=[("", "Categories")])
    taste_tag = forms.ChoiceField(
        required=False, choices=[("", "Taste tags")], label="Taste tag"
    )
    country = forms.ChoiceField(required=False, choices=[("", "Countries")])
    region = forms.ChoiceField(required=False, choices=[("", "Regions")])
    size = forms.ChoiceField(required=False, choices=[("", "Sizes")])
    vintage = forms.ChoiceField(required=False, choices=[("", "Vintages")])
    degree = forms.ChoiceField(required=False, choices=[("", "Degrees")])
    producer = forms.CharField(
        required=False, max_length=200, label="Producer"
    )  # need to discuss
    grape_variety = forms.CharField(
        required=False, max_length=200, label="Grape Variety"
    )  # need to discuss
    price_min = forms.DecimalField(
        required=False, max_digits=8, decimal_places=2, label="Minimum Price"
    )
    price_max = forms.DecimalField(
        required=False, max_digits=8, decimal_places=2, label="Maximum Price"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].choices += self._distinct_choices("category")
        self.fields["taste_tag"].choices += self._distinct_choices("taste_tag")
        self.fields["country"].choices += self._distinct_choices("country")
        self.fields["region"].choices += self._distinct_choices("region")
        self.fields["size"].choices += self._distinct_choices("size")
        self.fields["vintage"].choices += self._distinct_choices("vintage")
        self.fields["degree"].choices += self._distinct_choices("degree")

    @staticmethod
    def _distinct_choices(field_name: str):
        values = (
            Product.objects.exclude(**{field_name: ""})
            .exclude(**{field_name: None})
            .values_list(field_name, flat=True)
            .distinct()
            .order_by(field_name)
        )

        return [(v, v) for v in values]

    def clean(self):
        cleaned = super().clean()
        min_price = cleaned.get("price_min")
        max_price = cleaned.get("price_max")
        if min_price and max_price:
            if min_price > max_price:
                raise forms.ValidationError(
                    "Max price must be greater than or equal to min price."
                )
        return cleaned
