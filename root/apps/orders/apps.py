from django.apps import AppConfig

from root.core.utils import gettext_lazy as _


class AppOrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "root.apps.orders"
    verbose_name = _("Orders")
