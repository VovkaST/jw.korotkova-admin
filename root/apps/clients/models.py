from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField

from root.base.models import TimedModel
from root.core.enums import SocialsChoices


class Client(TimedModel):
    phone = PhoneNumberField(_("Phone number"), blank=True, unique=True, db_comment="Phone number without country code")
    surname = models.CharField(_("Surname"), max_length=255, db_comment="Client's surname")
    name = models.CharField(_("Name"), max_length=255, db_comment="Client's name")
    patronymic = models.CharField(
        _("Patronymic"), max_length=255, null=True, blank=True, db_comment="Client's patronymic (if exists)"
    )
    birth_date = models.DateField(_("Birth date"), null=True, blank=True, db_comment="Client's date of birth")

    class Meta:
        db_table = "jw_client"
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self):
        initials = [self.name[0].upper()]
        if self.patronymic:
            initials.append(self.patronymic[0].upper())
        return f"{self.surname} {'.'.join(initials)}. ({self.phone})"


class Social(TimedModel):
    social_type = models.CharField(
        _("Social type"), max_length=50, choices=SocialsChoices.choices, db_comment="Social type"
    )
    user_id = models.CharField(_("Telegram id"), max_length=50, null=True, blank=True, db_comment="Social id")
    username = models.CharField(_("Username"), max_length=255, null=True, blank=True, db_comment="Social username")
    client = models.ForeignKey(
        Client, verbose_name=_("Client"), on_delete=models.CASCADE, related_name="client_socials"
    )

    class Meta:
        db_table = "jw_social"
        verbose_name = _("Social")
        verbose_name_plural = _("Socials")
        unique_together = ("social_type", "client")
        constraints = [
            models.UniqueConstraint(
                fields=["social_type", "user_id"], condition=~Q(user_id=None), name="uq_jw_social_user_id"
            ),
            models.UniqueConstraint(
                fields=["social_type", "username"], condition=~Q(username=None), name="uq_jw_social_username"
            ),
        ]

    def __str__(self):
        return f"{self.social_type}: {self.username or self.user_id}"

    def clean(self):
        if not any((self.user_id, self.username)):
            raise ValidationError(_("Social id or social username must be set"))
        return super().clean()
