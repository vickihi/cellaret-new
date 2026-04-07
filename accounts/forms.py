from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
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
        self.fields["username"].widget.attrs.update(
            {"placeholder": _("Choose a username...")}
        )
        self.fields["password1"].widget.attrs.update(
            {"placeholder": _("Create a password...")}
        )
        self.fields["password2"].widget.attrs.update(
            {"placeholder": _("Confirm your password...")}
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("Enter username...")})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Enter password...")})
    )


class AccountProfileForm(forms.ModelForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(),
        label=_("Email address"),
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "id": "username",
                "placeholder": _("Enter username..."),
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "id": "user-email",
                "placeholder": _("No email provided"),
            }
        )
