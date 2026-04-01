from django.contrib.auth import get_user_model


User = get_user_model()


def create_user_account(*, username, email, password):
    normalized_email = (email or "").strip()

    return User.objects.create_user(
        username=username,
        email=normalized_email,
        password=password,
    )
