from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


UserModel = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Enter email..."}),
        label="Email",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Choose a username..."}
        )
        self.fields["password1"].widget.attrs.update(
            {"placeholder": "Create a password..."}
        )
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirm your password..."}
        )

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        if not email:
            raise forms.ValidationError("Email is required.")

        if UserModel._default_manager.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")

        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter username..."})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password..."})
    )


class AccountProfileForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(),
        label="Email address",
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "id": "username",
                "placeholder": "Enter username...",
                "readonly": "readonly",
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "id": "user-email",
                "placeholder": "No email provided",
                "readonly": "readonly",
            }
        )

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        if not email:
            raise forms.ValidationError("Email is required.")

        existing_users = UserModel._default_manager.filter(email__iexact=email)
        if self.instance.pk:
            existing_users = existing_users.exclude(pk=self.instance.pk)

        if existing_users.exists():
            raise forms.ValidationError("A user with that email already exists.")

        return email
