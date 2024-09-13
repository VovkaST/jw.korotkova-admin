from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppClientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "root.apps.clients"
    verbose_name = _("Client")
    verbose_name_plural = _("Clients")
