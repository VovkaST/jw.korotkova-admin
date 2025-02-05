from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
def format_empty(value, default: str = "&ndash;"):
    if value is None:
        return mark_safe(f"<center>{default}</center>")
    return value
