from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppClientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chair.app_clients"
    verbose_name = _("Clients")
