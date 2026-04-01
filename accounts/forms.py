from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": _("Enter email...")}),
        label=_("Email"),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css_classes} form-control".strip()

        self.fields["username"].widget.attrs.update(
            {"placeholder": _("Choose a username...")}
        )
        self.fields["password1"].widget.attrs.update(
            {"placeholder": _("Create a password...")}
        )
        self.fields["password2"].widget.attrs.update(
            {"placeholder": _("Confirm your password...")}
        )
