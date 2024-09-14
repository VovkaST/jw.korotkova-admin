from __future__ import annotations

from django.db.models import QuerySet
from django.db.models.base import ModelBase as DjangoModel
from pydantic import TypeAdapter

from root.base.entity import BaseEntity, BaseEntityType
from root.contrib.clean_architecture.interfaces import ObjectId
from root.core.utils import gettext_lazy as _


class BaseRepository:
    model: DjangoModel = None
    base_entity_class: type[BaseEntity] = None
    update_entity_class: type[BaseEntity] = None

    @property
    def objects(self):
        return self.model.objects

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

    def get_queryset(self):
        return self.model.objects.all()

    async def get(self, pk: ObjectId) -> base_entity_class:
        queryset = self.get_queryset()
        instance = queryset.get(pk=pk)
        return await self.to_entity(self.base_entity_class, instance)

    async def update(self, pk: ObjectId, dto: update_entity_class) -> ObjectId:
        instance = await self.objects.aget(pk=pk)
        # todo: Вычислить поля, входящие только в self.model, и закинуть их в include
        updated_data = dto.model_dump(exclude_unset=True, include={})
        update_fields = []
        for field_name, value in updated_data.items():
            if getattr(instance, field_name) != value:
                setattr(instance, field_name, value)
                update_fields.append(field_name)

        if update_fields:
            await instance.asave(update_fields=update_fields)
        return instance.pk
