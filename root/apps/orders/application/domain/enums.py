from django.db.models import TextChoices

from root.core.utils import gettext_lazy as _


class OrderStatusChoices(TextChoices):
    NEW = "NEW", _("New")
    IN_PROCESS = "IN_PROCESS", _("In process")
    PAYMENT_AWAIT = "PAYMENT_AWAIT", _("Waiting for payment")
    DELIVERY = "DELIVERY", _("Delivered")
    COMPLETED = "COMPLETED", _("Completed")
    CANCELLED = "CANCELLED", _("Canceled")


class DeliveryMethodChoices(TextChoices):
    PICKUP = "PICKUP", _("Pickup")
    YANDEX = "YANDEX", _("Yandex")
    RUSSIAN_POST = "RUSSIAN_POST", _("Russian Post")
    CDEK = "CDEK", _("CDEK")


class PaymentTypeChoices(TextChoices):
    PREPAYMENT = "PREPAYMENT", _("Prepayment")
    PARTIAL_PAYMENT = "PARTIAL_PAYMENT", _("Partial payment")
    FULL_PAYMENT = "FULL_PAYMENT", _("Full payment")
