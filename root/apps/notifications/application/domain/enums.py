from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class NotificationType(TextChoices):
    BIRTHDAY = "BIRTHDAY", _("Birthday")
