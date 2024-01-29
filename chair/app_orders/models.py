from django.core import validators
from django.db import models
from django.utils.translation import gettext as _

from chair.app_clients.models import Client
from chair.base.models import GUIDIdentifiedModel, IDIdentifiedModel, TimedModel


class Order(IDIdentifiedModel, TimedModel):
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
        validators=[validators.MinValueValidator(0)],
    )
    discount_sum = models.DecimalField(
        _("Sum of discount"),
        decimal_places=2,
        max_digits=10,
        db_comment="Sum of discount",
        editable=False,
        validators=[validators.MinValueValidator(0)],
    )
    discounted_sum = models.DecimalField(
        _("Discounted sum"),
        decimal_places=2,
        max_digits=10,
        db_comment="Sum with discount",
        editable=False,
        validators=[validators.MinValueValidator(0)],
    )
    tax_percent = models.IntegerField(
        _("Tax percent"),
        db_comment="Tax percent",
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)],
    )
    tax_sum = models.DecimalField(
        _("Tax sum"),
        decimal_places=2,
        max_digits=10,
        db_comment="Tax sum",
        editable=False,
        validators=[validators.MinValueValidator(0)],
    )

    class Meta:
        db_table = "jw_order"
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def clean(self):
        super().clean()
        self.discounted_sum = self.total_sum - self.discount_sum
        self.tax_sum = self.discounted_sum / 100 * self.tax_percent
