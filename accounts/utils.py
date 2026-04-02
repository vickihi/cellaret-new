from django.utils.http import url_has_allowed_host_and_scheme


DEFAULT_REDIRECT_URL_NAME = "products:catalog"
SIGNUP_NEXT_SESSION_KEY = "accounts_signup_next"


def get_valid_redirect_target(request, next_url):
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url

    return None


def store_signup_redirect_target(request, next_url):
    valid_target = get_valid_redirect_target(request, next_url)

    if valid_target:
        request.session[SIGNUP_NEXT_SESSION_KEY] = valid_target
    else:
        request.session.pop(SIGNUP_NEXT_SESSION_KEY, None)


def get_safe_redirect_target(request, default=DEFAULT_REDIRECT_URL_NAME):
    next_url = request.session.pop(SIGNUP_NEXT_SESSION_KEY, None)

    if next_url:
        return next_url

    return default
