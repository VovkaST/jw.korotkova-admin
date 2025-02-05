import uuid

from django.core import validators
from django.db import models
from django.utils import dateformat
from django.utils.safestring import mark_safe

from root.apps.orders.application.domain.enums import (
    DeliveryMethodChoices,
    OrderCategoryChoices,
    OrderStatusChoices,
    PaymentTypeChoices,
)
from root.base.models import TimedModel
from root.core.utils import gettext_lazy as _


class Order(TimedModel):
    guid = models.UUIDField(unique=True, default=uuid.uuid4)
    category = models.CharField(
        _("Category"), max_length=50, db_comment="Order category", choices=OrderCategoryChoices.choices
    )
    status = models.CharField(
        _("Order status"),
        max_length=50,
        db_comment="Order status",
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.NEW,
    )
    user = models.ForeignKey(
        "core.User",
        verbose_name=_("Client"),
        on_delete=models.CASCADE,
        related_name="order_client",
        null=True,
        blank=True,
    )
    discount = models.DecimalField(
        _("Percent of discount"),
        decimal_places=2,
        max_digits=5,
        db_comment="Percent of discount",
        default=0,
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)],
    )
    total_sum = models.DecimalField(
        _("Total order sum"),
        decimal_places=2,
        max_digits=10,
        db_comment="Total order sum",
        default=0,
        validators=[validators.MinValueValidator(0)],
    )
    discount_sum = models.DecimalField(
        _("Sum of discount"),
        decimal_places=2,
        max_digits=10,
        db_comment="Sum of discount",
        default=0,
        validators=[validators.MinValueValidator(0)],
    )
    discounted_sum = models.DecimalField(
        _("Sum with discount"),
        decimal_places=2,
        max_digits=10,
        db_comment="Sum with discount",
        default=0,
        validators=[validators.MinValueValidator(0)],
    )
    delivery_method = models.CharField(
        _("Delivery method"),
        max_length=50,
        db_comment="Delivery method",
        choices=DeliveryMethodChoices.choices,
        blank=True,
        null=True,
    )
    delivery_address = models.CharField(
        _("Delivery address"), max_length=255, null=True, blank=True, db_comment="Delivery address"
    )
    note = models.CharField(_("Note"), null=True, blank=True, db_comment="Note")

    class Meta:
        db_table = "jw_order"
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        category = OrderCategoryChoices(self.category)
        return mark_safe(f"{_('Order')} №{self.id}: {self.order_date} &ndash; {category.label}")

    @property
    def order_date(self) -> str:
        return dateformat.format(self.created_at, "d E Y, H:i")

    # def clean(self):
    #     self.discounted_sum = self.total_sum - self.discount_sum
    #     self.tax_sum = self.discounted_sum / 100 * self.tax_percent


class OrderItem(TimedModel):
    order = models.ForeignKey(Order, verbose_name=_("Order"), on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(
        "products.Product", verbose_name=_("Order"), on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.DecimalField(
        _("Item quantity"),
        decimal_places=2,
        max_digits=10,
        db_comment="Quantity of item in order",
        validators=[validators.MinValueValidator(0.01)],
    )
    price = models.DecimalField(
        _("Item price"),
        decimal_places=2,
        max_digits=10,
        db_comment="Order item price",
        validators=[validators.MinValueValidator(0)],
    )
    discount = models.DecimalField(
        _("Percent of discount"),
        decimal_places=2,
        max_digits=5,
        db_comment="Percent of discount",
        default=0,
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)],
    )
    total_sum = models.DecimalField(
        _("Total order sum"),
        decimal_places=2,
        max_digits=10,
        db_comment="Total order sum",
        default=0,
        validators=[validators.MinValueValidator(0)],
    )
    discount_sum = models.DecimalField(
        _("Sum of discount"),
        decimal_places=2,
        max_digits=10,
        db_comment="Sum of discount",
        default=0,
        validators=[validators.MinValueValidator(0)],
    )
    discounted_sum = models.DecimalField(
        _("Sum with discount"),
        decimal_places=2,
        max_digits=10,
        db_comment="Sum with discount",
        default=0,
        validators=[validators.MinValueValidator(0)],
    )

    class Meta:
        db_table = "jw_order_item"
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")

    # def clean(self):
    #     self.total_sum = self.price * self.quantity
    #     self.discounted_price = self.price * (Decimal(1) - self.discount_percent / Decimal(100))
    #     self.discounted_sum = self.discounted_price * self.quantity
    #     self.discount_sum = self.total_sum - self.discounted_sum


class OrderPayment(TimedModel):
    order = models.ForeignKey(Order, verbose_name=_("Order"), on_delete=models.CASCADE, related_name="order_payments")
    type = models.CharField(_("Type"), max_length=50, db_comment="Payment type", choices=PaymentTypeChoices.choices)
    sum = models.DecimalField(
        _("Payment sum"),
        decimal_places=2,
        max_digits=10,
        db_comment="Payment sum",
        validators=[validators.MinValueValidator(0.01)],
    )
    note = models.CharField(_("Note"), null=True, blank=True, db_comment="Note")

    class Meta:
        db_table = "jw_order_payment"
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
