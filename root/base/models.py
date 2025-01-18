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
        _("Creation date and time"), auto_now_add=True, db_comment="Creation date and time"
    )

    class Meta:
        abstract = True


class TimedModel(CreatedTimestampModel):
    """Родительский класс моделей для таблиц с полями дат создания и изменения"""

    updated_at = models.DateTimeField(_("Update date and time"), auto_now=True, db_comment="Update date and time")

    class Meta:
        abstract = True


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()
