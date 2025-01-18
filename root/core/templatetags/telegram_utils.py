from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def telegram_url(name_or_url: str, to_full: bool = True) -> str:
    """
    Tag for convert telegram url to short or full in depends of given argument `to_full`.
    """
    if name_or_url.startswith("@"):
        if not to_full:
            return name_or_url
        name = name_or_url[1:]
        return settings.TELEGRAM_URL_TEMPLATE.format(name=name)
    elif name_or_url.startswith(settings.TELEGRAM_URL):
        if not to_full:
            _url = name_or_url.removeprefix(f"{settings.TELEGRAM_URL}/")
            name = _url.split("/")[0]
            return f"@{name}"
        return name_or_url
    return f"@{name_or_url}"
