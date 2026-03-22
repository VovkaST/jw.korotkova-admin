from decimal import Decimal

from django.conf import settings
from django.contrib.postgres.fields import DateTimeRangeField
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from root.base.models import TimedModel


class Consultation(TimedModel):
    """История приёмов клиентов (консультаций)."""

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="consultations",
        verbose_name=_("Клиент"),
        db_comment="Клиент (пользователь)",
    )
    appointment_at = DateTimeRangeField(
        _("Интервал приёма"),
        db_index=True,
        db_comment="Интервал начала и окончания консультации (PostgreSQL tstzrange)",
        help_text=_("Укажите время начала и окончания консультации."),
    )
    description = models.TextField(
        _("Описание и результаты"),
        db_comment="Описание хода приёма и итоги (HTML из редактора)",
    )
    price = models.DecimalField(
        _("Стоимость консультации"),
        max_digits=10,
        decimal_places=2,
        default=Decimal("0"),
        validators=[validators.MinValueValidator(Decimal("0"))],
        db_comment="Стоимость консультации",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_consultations",
        verbose_name=_("Автор записи"),
        db_comment="Сотрудник, создавший запись в админке",
    )

    class Meta:
        db_table = "jw_consultation"
        ordering = ("-appointment_at",)
        verbose_name = _("Приём")
        verbose_name_plural = _("Приёмы")

    def __str__(self) -> str:
        client_name = self.client.get_full_name() or self.client.username
        r = self.appointment_at
        if r is None or getattr(r, "isempty", False):
            return str(client_name)
        lo, hi = r.lower, r.upper
        if lo is not None and hi is not None:
            return f"{client_name} — {lo:%d.%m.%Y %H:%M}–{hi:%H:%M}"
        if lo is not None:
            return f"{client_name} — с {lo:%d.%m.%Y %H:%M}"
        return str(client_name)
