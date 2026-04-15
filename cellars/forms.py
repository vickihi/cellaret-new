from django import forms

from cellars.models import Cellar


class CellarForm(forms.ModelForm):
    class Meta:
        model = Cellar
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        """Check if a cellar with the same name already exists for the user."""
        name = self.cleaned_data["name"]
        queryset = Cellar.objects.filter(name=name, user=self.user)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError("Cellar with this name already exists.")
        return name


class CellarBottleSortForm(forms.Form):
    SORT = [
        ("", "Default"),
        ("name_asc", "Name (A-Z)"),
        ("name_desc", "Name (Z-A)"),
        ("price_asc", "Price (low to high)"),
        ("price_desc", "Price (high to low)"),
        ("quantity_desc", "Quantity (high to low)"),
        ("quantity_asc", "Quantity (low to high)"),
    ]

    sort = forms.ChoiceField(
        label="Sort:",
        required=False,
        choices=SORT,
        initial="",
        widget=forms.Select(attrs={"class": "sort-select"}),
    )
