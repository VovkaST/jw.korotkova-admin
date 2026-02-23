from typing import ClassVar

from django.db import models

from root.base.entity import BaseEntityType


class SingletonModel(models.Model):
    instance = None
    entity_class: ClassVar[type[BaseEntityType]]  # pyright: ignore[reportGeneralTypeIssues]

    class Meta:
        abstract = True

    def __new__(cls, *args, **kwargs):
        if args or kwargs:
            return super().__new__(cls)

        if not cls.instance or not cls.instance.id:
            cls.instance, created = cls.objects.get_or_create(id=1)
        else:
            cls.instance.refresh_from_db()

        return cls.instance

    def __init__(self, *args, **kwargs):
        if args or kwargs:
            super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return (0, {})

    def as_entity(self) -> BaseEntityType:
        return self.entity_class.model_validate(self, from_attributes=True)
