from django.db.models import TextChoices

from root.core.utils import gettext_lazy as _
from root.core.utils import pgettext_lazy


class OrderCategoryChoices(TextChoices):
    MAKING_JEWELRY = "MAKING_JEWELRY", _("Making jewelry")
    SALE = "SALE", _("Sale")


class OrderStatusChoices(TextChoices):
    NEW = "NEW", pgettext_lazy("Order", "New")
    IN_PROCESS = "IN_PROCESS", _("In process")
    PAYMENT_AWAIT = "PAYMENT_AWAIT", _("Waiting for payment")
    DELIVERY = "DELIVERY", _("Delivered")
    COMPLETED = "COMPLETED", _("Completed")
    CANCELLED = "CANCELLED", _("Canceled")


class OrderActionsChoices(TextChoices):
    PROCESS = "PROCESS", _("To process")
    PAYMENT = "PAYMENT", _("To payment")
    DELIVERY = "DELIVERY", _("Delivery")
    COMPLETE = "COMPLETE", _("Complete")
    CANCEL = "CANCEL", _("Cancel")


ActionsMap = {
    OrderActionsChoices.PROCESS: OrderStatusChoices.IN_PROCESS,
    OrderActionsChoices.PAYMENT: OrderStatusChoices.PAYMENT_AWAIT,
    OrderActionsChoices.DELIVERY: OrderStatusChoices.DELIVERY,
    OrderActionsChoices.COMPLETE: OrderStatusChoices.COMPLETED,
    OrderActionsChoices.CANCEL: OrderStatusChoices.CANCELLED,
}


class DeliveryMethodChoices(TextChoices):
    PICKUP = "PICKUP", _("Pickup")
    YANDEX = "YANDEX", _("Yandex")
    RUSSIAN_POST = "RUSSIAN_POST", _("Russian Post")
    CDEK = "CDEK", _("CDEK")


class PaymentTypeChoices(TextChoices):
    PREPAYMENT = "PREPAYMENT", _("Prepayment")
    PARTIAL_PAYMENT = "PARTIAL_PAYMENT", _("Partial payment")
    FULL_PAYMENT = "FULL_PAYMENT", _("Full payment")
    REFUND = "REFUND", _("Refund")
