import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class GUIDIdentifiedModel(models.Model):
    """Родительский класс моделей таблиц БД, где идентификатором является поле guid типа uuid4"""

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True


class CreatedTimestampModel(models.Model):
    """Родительский класс моделей для таблиц с полями даты создания"""

    created_at = models.DateTimeField(
        _("Creation date and time"), auto_now_add=True, db_comment=_("Creation date and time")
    )

    class Meta:
        abstract = True


class TimedModel(CreatedTimestampModel):
    """Родительский класс моделей для таблиц с полями дат создания и изменения"""

    updated_at = models.DateTimeField(_("Update date and time"), auto_now=True, db_comment=_("Update date and time"))

    class Meta:
        abstract = True
