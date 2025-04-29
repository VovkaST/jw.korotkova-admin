from contextlib import suppress

from django import template

from root.apps.orders.application.domain.enums import DeliveryMethodChoices, PaymentTypeChoices

register = template.Library()


def format_enum(enum_class, value):
    with suppress(ValueError):
        return str(enum_class(value).label)
    return ""


@register.filter(is_safe=True)
def format_payment_type(value: str) -> str:
    return format_enum(PaymentTypeChoices, value)


@register.filter(is_safe=True)
def format_delivery_method(value: str) -> str:
    return format_enum(DeliveryMethodChoices, value)
