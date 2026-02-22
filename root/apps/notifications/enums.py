from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class NotificationType(TextChoices):
    email = "EMAIL", _("Email")
    telegram = "TELEGRAM", _("Telegram")


class NotificationStatus(TextChoices):
    NEW = "NEW", _("New")
    SENT = "SENT", _("Sent")
    ERROR = "ERROR", _("Error")


class NotificationDailyType(TextChoices):
    BIRTHDAY = "BIRTHDAY", _("Birthday")
