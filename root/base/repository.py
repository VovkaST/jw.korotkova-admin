from __future__ import annotations

from django.db.models import QuerySet
from django.db.models.base import ModelBase as DjangoModel
from pydantic import TypeAdapter

from root.base.entity import BaseEntity, BaseEntityType
from root.core.utils import gettext_lazy as _


class BaseRepository:
    model: DjangoModel = None

    @staticmethod
    def _model_to_entity(entity_class: type[BaseEntity], obj: DjangoModel, from_attributes: bool = True) -> BaseEntity:
        assert issubclass(entity_class, BaseEntity), _("Entity must be a subclass of BaseEntity")
        return TypeAdapter(entity_class).validate_python(obj, from_attributes=from_attributes)

    async def to_entity(
        self, entity_class: type[BaseEntity], obj: DjangoModel, from_attributes: bool = True
    ) -> BaseEntityType:
        return self._model_to_entity(entity_class, obj, from_attributes=from_attributes)

    async def to_entities(
        self, entity_class: type[BaseEntity], queryset: QuerySet, from_attributes: bool = True
    ) -> list[BaseEntityType]:
        return [
            self._model_to_entity(entity_class, instance, from_attributes=from_attributes)
            async for instance in queryset.aiterator()
        ]
