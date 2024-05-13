from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "root.apps.bot"
    verbose_name = _("Bot")
    verbose_name_plural = _("Bots")
