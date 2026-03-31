from django import forms


class ProductCatalogSearchForm(forms.Form):
    q = forms.CharField(
        label="Search products",
        max_length=200,
        required=False,
        strip=True,
    )


class ProductSortForm(forms.Form):
    SORT = [
        ("default", "Relevance"),
        ("price_asc", "Price (low to high)"),
        ("price_desc", "Price (high to low)"),
        ("name_asc", "Name (A-Z)"),
        ("name_desc", "Name (Z-A)"),
    ]

    sort = forms.ChoiceField(
        label="Sort:",
        required=False,
        choices=SORT,
        initial="default",
        widget=forms.Select(attrs={"class": "sort-select"}),
    )
