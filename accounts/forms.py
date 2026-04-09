from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    UserCreationForm,
)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


UserModel = get_user_model()


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


class UsernameEmailPasswordResetForm(PasswordResetForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": _("Enter username...")}),
        label=_("Username"),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": _("Enter email...")}),
        label=_("Email"),
    )

    default_error_messages = {
        "invalid_credentials": _(
            "We couldn't match that username and email to an account."
        ),
    }

    def clean(self):
        cleaned_data = super().clean()
        username = (cleaned_data.get("username") or "").strip()
        email = (cleaned_data.get("email") or "").strip()

        self.user = None

        if not username or not email:
            return cleaned_data

        try:
            user = UserModel._default_manager.get(username=username)
        except UserModel.DoesNotExist:
            raise forms.ValidationError(
                self.error_messages["invalid_credentials"],
            )

        if (user.email or "").strip().lower() != email.lower():
            raise forms.ValidationError(
                self.error_messages["invalid_credentials"],
            )

        self.user = user
        return cleaned_data

    def get_users(self, email):
        if not getattr(self, "user", None):
            return []

        user = self.user
        if not user.is_active or not user.has_usable_password():
            return []

        return [user]
