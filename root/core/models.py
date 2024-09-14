from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """User's model"""

    patronymic = models.CharField(_("Patronymic"), max_length=150, blank=True, null=True, db_comment="Patronymic")
    phone = PhoneNumberField(_("Phone number"), blank=True, null=True, unique=True, db_comment="Phone number")
    telegram_id = models.CharField(
        _("Telegram id"), max_length=50, null=True, blank=True, unique=True, db_comment="Telegram id"
    )

    class Meta:
        db_table = "auth_user"
        db_table_comment = "Users"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def clean(self):
        if self.telegram_id and not self.telegram_id.startswith("@"):
            self.telegram_id = f"@{self.telegram_id}"
