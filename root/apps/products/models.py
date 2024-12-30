import uuid

from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from root.apps.products.managers import ProductQuerySet, ProductTypeQuerySet
from root.apps.products.utils import upload_product_file_to
from root.base.models import CreatedTimestampModel, TimedModel


class ProductType(models.Model):
    name = models.CharField(_("Unique name"), max_length=255, unique=True, db_comment="Product type name")
    description = models.CharField(
        _("Description"), null=True, blank=True, max_length=1000, db_comment="Product type description"
    )
    is_active = models.BooleanField(_("Is active"), default=True, db_comment="Is product type active")

    objects = ProductTypeQuerySet.as_manager()

    class Meta:
        db_table = "jw_product_type"
        verbose_name = _("Product type")
        verbose_name_plural = _("Product types")

    def __str__(self):
        if not self.is_active:
            return f"{self.name} ({_('not active')})"
        return self.name


class Product(TimedModel):
    guid = models.UUIDField(unique=True, default=uuid.uuid4)
    type = models.ForeignKey(
        ProductType, on_delete=models.PROTECT, verbose_name=_("Product type"), db_comment="Product type"
    )
    title = models.CharField(_("Unique name"), max_length=255, unique=True, db_comment="Product unique name")
    description = models.CharField(_("Description"), max_length=1000, db_comment="Product`s description")
    price = models.DecimalField(
        _("Price"),
        decimal_places=2,
        max_digits=10,
        db_comment="Price",
        default=0,
        validators=[validators.MinValueValidator(0)],
    )
    in_stock = models.BooleanField(_("In stock"), default=True, db_comment="Is product in stock")

    objects = ProductQuerySet.as_manager()

    class Meta:
        db_table = "jw_product"
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return f'{self.type.name} "{self.title}"'


class ProductFiles(CreatedTimestampModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        editable=False,
        related_name="files",
        db_comment="Product",
    )
    file = models.FileField(verbose_name=_("File's link"), upload_to=upload_product_file_to)
    description = models.CharField(
        _("Description"), null=True, blank=True, max_length=1000, db_comment="File`s description"
    )

    class Meta:
        db_table = "jw_product_files"
        verbose_name = _("Product file")
        verbose_name_plural = _("Product files")

    def __str__(self):
        return self.description or self.file.url


class ProductPriceHistory(CreatedTimestampModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        editable=False,
        related_name="price_history",
        db_comment="Product",
    )
    price = models.DecimalField(
        _("Price"),
        decimal_places=2,
        max_digits=10,
        db_comment="Price",
        editable=False,
        default=0,
        validators=[validators.MinValueValidator(0)],
    )

    class Meta:
        db_table = "jw_product_price_history"
        verbose_name = _("Product price history")
        verbose_name_plural = _("Product price history")
