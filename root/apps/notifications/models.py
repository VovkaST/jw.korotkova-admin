from django.db import models
from django.utils.translation import gettext_lazy as _

from root.apps.notifications.application.domain.enums import NotificationType
from root.base.models import TimedModel


class NotificationDaily(TimedModel):
    """
    Daily notifications
    """

    mailing_name = models.CharField(verbose_name=_("Mailing name"), max_length=255, unique=True)
    type = models.CharField(verbose_name=_("Type"), max_length=255, choices=NotificationType.choices)
    by_email = models.BooleanField(
        verbose_name=_("By e-mail"), help_text=_("Send notification by e-mail"), default=False
    )
    by_telegram = models.BooleanField(
        verbose_name=_("By Telegram"), help_text=_("Send notification by Telegram"), default=False
    )
    is_active = models.BooleanField(verbose_name=_("Is active"), default=True)
    users = models.ManyToManyField(verbose_name=_("Users"), to="core.User", related_name="notifications_daily")

    class Meta:
        db_table = "jw_notifications_daily"
        unique_together = ("type", "is_active")
        verbose_name = _("Daily notification")
        verbose_name_plural = _("Daily notifications")

    def __str__(self):
        return f"{self.mailing_name} ({self.type})"
