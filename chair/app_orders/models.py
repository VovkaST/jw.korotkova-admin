from decimal import Decimal

from django.core import validators
from django.db import models
from django.utils.translation import gettext as _

from chair.app_clients.models import Client
from chair.base.models import GUIDIdentifiedModel, TimedModel


class Order(GUIDIdentifiedModel, TimedModel):
    client_guid = models.ForeignKey(
        Client,
        verbose_name=_("Client GUID"),
        on_delete=models.CASCADE,
        related_name="order_client",
        db_column="client_guid",
    )
    total_sum = models.DecimalField(
        _("Total order sum"),
        decimal_places=2,
        max_digits=10,
        db_comment="Total order sum",
        editable=False,
        default=0,
        validators=[validators.MinValueValidator(0)],
    )
    discount_sum = models.DecimalField(
        _("Sum of discount"),
        decimal_places=2,
        max_digits=10,
        db_comment="Sum of discount",
        editable=False,
        default=0,
        validators=[validators.MinValueValidator(0)],
    )
    discounted_sum = models.DecimalField(
        _("Discounted sum"),
        decimal_places=2,
        max_digits=10,
        db_comment="Sum with discount",
        editable=False,
        default=0,
        validators=[validators.MinValueValidator(0)],
    )
    tax_percent = models.IntegerField(
        _("Tax percent"),
        db_comment="Tax percent",
        default=0,
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)],
    )
    tax_sum = models.DecimalField(
        _("Tax sum"),
        decimal_places=2,
        max_digits=10,
        db_comment="Tax sum",
        editable=False,
        default=0,
        validators=[validators.MinValueValidator(0)],
    )

    class Meta:
        db_table = "jw_order"
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"{_('Order')} №{self.guid} {_('from')} {self.created_at}"

    # def clean(self):
    #     self.discounted_sum = self.total_sum - self.discount_sum
    #     self.tax_sum = self.discounted_sum / 100 * self.tax_percent


class OrderItem(TimedModel):
    order = models.ForeignKey(
        "Order",
        verbose_name=_("Parent order"),
        on_delete=models.CASCADE,
        related_name="order_items",
    )
    item_name = models.CharField(_("Item name"), max_length=255, db_comment="Item name")
    price = models.DecimalField(
        _("Item price"),
        decimal_places=2,
        max_digits=10,
        db_comment="Order item price",
        validators=[validators.MinValueValidator(0)],
    )
    quantity = models.DecimalField(
        _("Item quantity"),
        decimal_places=2,
        max_digits=10,
        db_comment="Quantity of item in order",
        validators=[validators.MinValueValidator(0.01)],
    )
    total_sum = models.DecimalField(
        _("Total item sum"),
        decimal_places=2,
        max_digits=10,
        db_comment="Total item sum",
        editable=False,
        validators=[validators.MinValueValidator(0)],
    )
    discount_percent = models.IntegerField(
        _("Discount percent"),
        default=0,
        db_comment="Discount percent",
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)],
    )
    discounted_price = models.DecimalField(
        _("Discounted price of item"),
        decimal_places=2,
        max_digits=10,
        db_comment="Price of item with discount",
        editable=False,
        validators=[validators.MinValueValidator(0)],
    )
    discount_sum = models.DecimalField(
        _("Sum of item discount"),
        decimal_places=2,
        max_digits=10,
        db_comment="Sum of item discount",
        editable=False,
        validators=[validators.MinValueValidator(0)],
    )
    discounted_sum = models.DecimalField(
        _("Discounted item sum"),
        decimal_places=2,
        max_digits=10,
        db_comment="Item's sum with discount",
        editable=False,
        validators=[validators.MinValueValidator(0)],
    )

    class Meta:
        db_table = "jw_order_item"
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")

    def clean(self):
        self.total_sum = self.price * self.quantity
        self.discounted_price = self.price * (Decimal(1) - self.discount_percent / Decimal(100))
        self.discounted_sum = self.discounted_price * self.quantity
        self.discount_sum = self.total_sum - self.discounted_sum
