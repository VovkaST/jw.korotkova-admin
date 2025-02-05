from __future__ import annotations

from django.db.models import QuerySet
from django.db.models.base import ModelBase as DjangoModel
from pydantic import BaseModel

from root.base.entity import BaseEntity, BaseEntityType
from root.base.interfaces import IBaseRepository
from root.contrib.clean_architecture.interfaces import ObjectId
from root.contrib.clean_architecture.utils import create_entity_object
from root.core.utils import Singleton
from root.core.utils import gettext_lazy as _


class BaseRepository(Singleton, IBaseRepository):
    model: DjangoModel = None
    base_entity_class: type[BaseEntity] = None
    update_dto_class: type[BaseModel] = None

    @property
    def objects(self):
        return self.model.objects

    @staticmethod
    async def _model_to_entity(
        entity_class: type[BaseEntity],
        obj: DjangoModel,
        mappings: dict[str, str] | None = None,
        exclude: set | list | tuple = None,
        depth: int = 0,
        include_relation: set | list | tuple = None,
    ) -> BaseEntity:
        assert issubclass(entity_class, BaseEntity), _("Entity must be a subclass of BaseEntity")
        return await create_entity_object(
            entity_class, obj, mappings=mappings, exclude=exclude, depth=depth, include_relation=include_relation
        )

    async def to_entity(
        self,
        entity_class: type[BaseEntity],
        obj: DjangoModel,
        mappings: dict[str, str] | None = None,
        exclude: set | list | tuple = None,
        depth: int = 0,
        include_relation: set | list | tuple = None,
    ) -> BaseEntityType:
        return await self._model_to_entity(
            entity_class, obj, mappings=mappings, exclude=exclude, depth=depth, include_relation=include_relation
        )

    async def to_entities(
        self,
        entity_class: type[BaseEntity],
        queryset: QuerySet,
        mappings: dict[str, str] | None = None,
        exclude: set | list | tuple = None,
        depth: int = 0,
        include_relation: set | list | tuple = None,
    ) -> list[BaseEntityType]:
        return [
            await self._model_to_entity(
                entity_class,
                instance,
                mappings=mappings,
                exclude=exclude,
                depth=depth,
                include_relation=include_relation,
            )
            async for instance in queryset.aiterator()
        ]

    def get_queryset(self) -> QuerySet:
        return self.model.objects.all()

    def get_model_field_names(self, model: DjangoModel) -> set[str]:
        return {f.column for f in model._meta.fields if not f.primary_key}

    async def create(self, **kwargs) -> base_entity_class:
        instance = await self.model.objects.acreate(**kwargs)
        return await self.to_entity(self.base_entity_class, instance)

    async def get(self, pk: ObjectId) -> base_entity_class:
        queryset = self.get_queryset()
        instance = await queryset.aget(pk=pk)
        return await self.to_entity(self.base_entity_class, instance)

    async def update(self, pk: ObjectId, dto: update_dto_class) -> ObjectId:
        instance = await self.objects.aget(pk=pk)
        real_fields = self.get_model_field_names(self.model)
        updated_data = dto.model_dump(exclude_unset=True, include=real_fields)
        update_fields = []
        for field_name, value in updated_data.items():
            if getattr(instance, field_name) != value:
                setattr(instance, field_name, value)
                update_fields.append(field_name)

        if update_fields:
            await instance.asave(update_fields=update_fields)
        return instance.pk

    async def delete(self, **kwargs) -> tuple[int, dict[str, int]]:
        return await self.model.objects.filter(**kwargs).adelete()
