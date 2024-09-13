from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppNotificationsDailyConfig(AppConfig):
    name = "root.apps.notifications"
    verbose_name = _("Notification")
    verbose_name_plural = _("Notifications")
