from __future__ import annotations

from collections.abc import Iterable

from root.apps.products.application.boundaries import IProductChannelPublicationRepository
from root.apps.products.application.boundaries.dtos import (
    ProductChannelPublicationCreateDTO,
    ProductChannelPublicationUpdateDTO,
)
from root.apps.products.application.domain.entities import ProductChannelPublicationEntity
from root.apps.products.models import ProductChannelPublication
from root.base.repository import BaseRepository


class ProductChannelPublicationRepository(BaseRepository, IProductChannelPublicationRepository):
    model = ProductChannelPublication
    base_entity_class = ProductChannelPublicationEntity
    update_dto_class = ProductChannelPublicationUpdateDTO

    async def create(self, dto: ProductChannelPublicationCreateDTO) -> base_entity_class:
        return await super().create(**dto.model_dump())

    async def delete(self, channel_id: int, message_id: int, product_ids: Iterable[int]) -> tuple[int, dict[str, int]]:
        return await super().delete(channel_id=channel_id, message_id=message_id, product_id__in=product_ids)

    async def get_product_publications(self, product_id: int) -> list[ProductChannelPublicationEntity]:
        """Get all product publications"""
        publications = await self.get_queryset().filter(product_id=product_id)
        return await self.to_entities(self.base_entity_class, publications)

    async def get_products_publications(
        self, product_ids: Iterable[int], order_by: list[str] = None
    ) -> list[ProductChannelPublicationEntity]:
        """Get all publications of given products"""
        order_by = order_by or ["id"]
        publications = self.get_queryset().filter(product_id__in=product_ids).order_by(*order_by)
        return await self.to_entities(self.base_entity_class, publications)

    async def get_message_mentions(self, message_id: int) -> list[ProductChannelPublicationEntity]:
        """Get all publications mentions in given message"""
        publications = self.get_queryset().filter(message_id=message_id)
        return await self.to_entities(self.base_entity_class, publications)
