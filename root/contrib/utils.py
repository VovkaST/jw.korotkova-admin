from inspect import isfunction

from django.apps import apps
from django.conf import settings
from django.contrib.sites.requests import RequestSite


def dotval(obj, dottedpath, default=None):
    """
    Возвращает значение аттрибута объекта или элемента словаря по его пути в формате 'a.b.c'
    Примеры:
    obj = {'item1': {'nested': 123, 'other': 456}}
    >>> dotval(obj, "item1.nested")
    123
    >>> dotval(obj, "item2")
    None
    """
    val = obj
    sentinel = object()
    for attr in dottedpath.split("."):
        if isinstance(val, dict):
            val = val.get(attr, sentinel)
            if val is sentinel:
                return default
        elif not hasattr(val, attr):
            return default
        else:
            val = getattr(val, attr, sentinel)
            if val is sentinel:
                return default
            if isfunction(val):
                val = val()
    return val


def get_current_site(request=None):
    if apps.is_installed("django.contrib.sites"):
        from django.contrib.sites.models import Site

        return Site.objects.get_current(request)
    if request is not None:
        return RequestSite(request)


def resource_url(url: str) -> str:
    """
    Возвращает полный url для ресурса сайта
    """
    if not url.startswith("/"):
        url = f"/{url}"
    site = get_current_site()
    schema = "https" if settings.USE_SITE_SECURED_PROTOCOL else "http"
    return f"{schema}://{site.domain}{url}"
