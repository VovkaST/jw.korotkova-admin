from __future__ import annotations

from collections.abc import Iterable

from django.db.models import QuerySet

from root.apps.products.dtos import (
    ProductChannelPublicationCreateDTO,
    ProductChannelPublicationUpdateDTO,
)
from root.apps.products.models import ProductChannelPublication
from root.base.repository import BaseRepository
from root.core.types import DeleteResult


class ProductChannelPublicationRepository(BaseRepository[ProductChannelPublication]):
    model = ProductChannelPublication

    def get_queryset(self) -> QuerySet[ProductChannelPublication]:
        return self.model.objects.all()

    @staticmethod
    def _get_model_field_names(model: type[ProductChannelPublication]) -> set[str]:
        return {f.column for f in model._meta.fields if not f.primary_key}

    async def create(self, dto: ProductChannelPublicationCreateDTO) -> ProductChannelPublication:
        instance = await self.model.objects.acreate(**dto.model_dump())
        return instance

    async def update(
        self,
        pk: int,
        dto: ProductChannelPublicationUpdateDTO,
    ) -> int:
        instance = await self.model.objects.aget(pk=pk)
        real_fields = self._get_model_field_names(self.model)
        updated_data = dto.model_dump(exclude_unset=True)
        update_fields = [
            name for name in updated_data if name in real_fields and getattr(instance, name) != updated_data[name]
        ]
        for name in update_fields:
            setattr(instance, name, updated_data[name])
        if update_fields:
            await instance.asave(update_fields=update_fields)
        return instance.pk

    async def delete(
        self,
        channel_id: int,
        message_id: int,
        product_ids: Iterable[int],
    ) -> DeleteResult:
        return await self.model.objects.filter(
            channel_id=channel_id, message_id=message_id, product_id__in=product_ids
        ).adelete()

    def get_products_publications(
        self,
        product_ids: Iterable[int],
        order_by: list[str] | None = None,
    ) -> QuerySet[ProductChannelPublication]:
        order_by = order_by or ["id"]
        return self.get_queryset().filter(product_id__in=product_ids).order_by(*order_by)

    def get_message_mentions(self, message_id: int) -> QuerySet[ProductChannelPublication]:
        return self.get_queryset().filter(message_id=message_id)
