from django.utils.http import url_has_allowed_host_and_scheme


DEFAULT_REDIRECT_URL_NAME = "products:catalog"


def get_safe_redirect_target(request, default=DEFAULT_REDIRECT_URL_NAME):
    next_url = request.POST.get("next") or request.GET.get("next")

    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url

    return default
