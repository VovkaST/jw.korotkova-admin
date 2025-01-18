from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from root.base.models import SingletonModel, TimedModel
from root.core.enums import SocialsChoices


class SiteSettings(SingletonModel):
    """Site settings singleton models"""

    title = models.CharField(_("Site title"), max_length=255, blank=True, null=True, db_comment="Site title")
    description = models.CharField(_("Site description"), blank=True, null=True, db_comment="Site description")
    tm_label = models.CharField(_("Trade mark label"), blank=True, null=True, db_comment="Trade mark label")
    yandex_metrika = models.CharField(
        _("Code of Yandex metrika widget"), blank=True, null=True, db_comment="Code of Yandex metrika widget"
    )
    telegram_channel = models.CharField(
        _("Telegram channel name"), max_length=100, blank=True, null=True, db_comment="Telegram channel name"
    )
    telegram_channel_description = models.CharField(
        _("Telegram channel description"), blank=True, null=True, db_comment="Telegram channel description"
    )

    class Meta:
        db_table = "jw_settings"
        db_table_comment = "Site dynamic settings"
        verbose_name = _("Settings")
        verbose_name_plural = _("Settings")


class User(AbstractUser):
    """User's model"""

    patronymic = models.CharField(_("Patronymic"), max_length=150, blank=True, null=True, db_comment="Patronymic")
    phone = PhoneNumberField(_("Phone number"), blank=True, null=True, unique=True, db_comment="Phone number")
    birth_date = models.DateField(_("Birth date"), null=True, blank=True, db_comment="User's date of birth")

    class Meta:
        db_table = "auth_user"
        db_table_comment = "Users"
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class UserSocial(TimedModel):
    social_type = models.CharField(
        _("Social type"), max_length=50, choices=SocialsChoices.choices, db_comment="Social type"
    )
    social_user_id = models.CharField(_("Telegram id"), max_length=50, null=True, blank=True, db_comment="Social id")
    social_username = models.CharField(
        _("Username"), max_length=255, null=True, blank=True, db_comment="Social username"
    )
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="socials")

    class Meta:
        db_table = "jw_user_social"
        verbose_name = _("User social")
        verbose_name_plural = _("User socials")
        unique_together = ("social_type", "user")
        constraints = [
            models.UniqueConstraint(
                fields=["social_type", "social_user_id"],
                condition=~Q(social_user_id=None),
                name="unique_social_user_id",
            ),
            models.UniqueConstraint(
                fields=["social_type", "social_username"],
                condition=~Q(social_username=None),
                name="unique_social_username",
            ),
        ]

    def __str__(self):
        return f"{self.social_type}: {self.social_username or self.social_user_id}"

    def clean(self):
        if not any((self.social_user_id, self.social_username)):
            raise ValidationError(_("Social user id or social username must be set"))
        return super().clean()
