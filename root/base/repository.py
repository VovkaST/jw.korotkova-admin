from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar, Generic, TypeVar

from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from django.db.models.base import Model

from root.base.entity import BaseDTOType, BaseEntity, BaseEntityType
from root.contrib.clean_architecture.interfaces import ObjectId
from root.core.types import DeleteResult
from root.core.utils import Singleton
from root.core.utils import gettext_lazy as _

T = TypeVar("T", bound=Model)


class BaseRepository(Singleton, Generic[T]):
    model: ClassVar[type[T]]
    base_entity_class: type[BaseEntityType]
    update_dto_class: type[BaseDTOType]

    @property
    def objects(self) -> QuerySet[T]:
        return self.model.objects.all()

    @staticmethod
    async def _model_to_entity(entity_class: type[BaseEntityType], obj: Model, from_attributes: bool) -> BaseEntityType:
        assert issubclass(entity_class, BaseEntity), _("Entity must be a subclass of BaseEntity")
        return await sync_to_async(entity_class.model_validate)(obj, from_attributes=from_attributes)

    async def to_entity(
        self, entity_class: type[BaseEntityType], obj: Model, from_attributes: bool = True
    ) -> BaseEntityType:
        return await self._model_to_entity(entity_class, obj, from_attributes=from_attributes)

    async def to_entities(
        self, entity_class: type[BaseEntityType], queryset: QuerySet, from_attributes: bool = True
    ) -> Sequence[BaseEntityType]:
        return [
            await self._model_to_entity(entity_class, instance, from_attributes=from_attributes)
            async for instance in queryset.all()
        ]

    def get_queryset(self) -> QuerySet[T]:
        return self.objects.all()

    def get_model_field_names(self, model: Model) -> set[str]:
        return {f.column for f in model._meta.fields if not f.primary_key}

    async def create(self, **kwargs) -> BaseEntity:
        instance = await self.model.objects.acreate(**kwargs)
        return await self.to_entity(self.base_entity_class, instance)

    async def get(self, pk: ObjectId) -> BaseEntity:
        queryset = self.get_queryset()
        instance = await queryset.aget(pk=pk)
        return await self.to_entity(self.base_entity_class, instance)

    async def update(self, pk: ObjectId, dto: BaseDTOType) -> ObjectId:
        instance = await self.objects.aget(pk=pk)
        real_fields = self.get_model_field_names(self.model)
        updated_data = dto.model_dump(exclude_unset=True, include=real_fields - {"id"})
        update_fields = []
        for field_name, value in updated_data.items():
            if getattr(instance, field_name) != value:
                setattr(instance, field_name, value)
                update_fields.append(field_name)

        if update_fields:
            await instance.asave(update_fields=update_fields)
        return instance.pk

    async def bulk_update(self, dtos: list[BaseDTOType]) -> list[ObjectId]:
        qs = self.objects.filter(pk__in=[dto.id for dto in dtos])  # pyright: ignore[reportAttributeAccessIssue]
        instance_by_id = {instance.pk: instance for instance in qs}
        real_fields = self.get_model_field_names(self.model)
        update_fields = set()
        instance_for_update = []

        for dto in dtos:
            instance = instance_by_id.get(dto.id)  # pyright: ignore[reportAttributeAccessIssue]

            if not instance:
                continue

            updated_data = dto.model_dump(exclude_unset=True, include=real_fields - {"id"})
            for field_name, value in updated_data.items():
                if getattr(instance, field_name) != value:
                    setattr(instance, field_name, value)
                    update_fields.add(field_name)
            instance_for_update.append(instance)

        await self.objects.abulk_update(instance_for_update, fields=list(update_fields))
        return [instance.pk for instance in instance_for_update]

    async def delete(self, **kwargs) -> DeleteResult:
        return await self.objects.filter(**kwargs).adelete()
