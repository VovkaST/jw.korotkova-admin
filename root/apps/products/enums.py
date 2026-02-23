from django.db.models import TextChoices

from root.core.utils import gettext_lazy as _


class ProductCategoryChoices(TextChoices):
    PRODUCT = "PRODUCT", _("Product")
    SERVICE = "SERVICE", _("Service")
