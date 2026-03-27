from django import forms


class ProductCatalogSearchForm(forms.Form):
    q = forms.CharField(
        label="Search products",
        max_length=200,
        required=False,
        strip=True,
    )
