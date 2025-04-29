from __future__ import annotations

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


class PaymentStatusChoices(TextChoices):
    NOT_PAID = "NOT_PAID", _("Not paid")
    PARTIALLY_PAID = "PARTIALLY_PAID", _("Partially paid")
    PAID = "PAID", _("Paid")
    DEBT = "DEBT", _("Debt")
    OVERPAID = "OVERPAID", _("Overpaid")
    # REFUNDED = "REFUNDED", _("Refunded")
    # PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED", _("Partially refunded")


class PaymentTypeChoices(TextChoices):
    PREPAYMENT = "PREPAYMENT", _("Prepayment")
    PARTIAL_PAYMENT = "PARTIAL_PAYMENT", _("Partial payment")
    FULL_PAYMENT = "FULL_PAYMENT", _("Full payment")
    REFUND = "REFUND", _("Refund")

    @classmethod
    def consumption_types(cls) -> list[PaymentTypeChoices]:
        return [cls.REFUND]

    @classmethod
    def income_types(cls) -> list[PaymentTypeChoices]:
        return [cls.PREPAYMENT, cls.PARTIAL_PAYMENT, cls.FULL_PAYMENT]
