from __future__ import annotations

from root.apps.products.application.boundaries import IProductChannelPublicationRepository
from root.apps.products.application.boundaries.dtos import ProductChannelPublicationCreateDTO
from root.apps.products.application.domain.entities import ProductChannelPublicationEntity
from root.apps.products.models import ProductChannelPublication
from root.base.repository import BaseRepository


class ProductChannelPublicationRepository(BaseRepository, IProductChannelPublicationRepository):
    model = ProductChannelPublication
    base_entity_class = ProductChannelPublicationEntity

    async def create(self, dto: ProductChannelPublicationCreateDTO) -> base_entity_class:
        return await super().create(**dto.model_dump())

    async def get_product_publications(self, product_id: int) -> list[ProductChannelPublicationEntity]:
        """Get all product publications"""
        publications = await self.get_queryset().filter(product_id=product_id)
        return await self.to_entities(self.base_entity_class, publications)

    async def get_products_publications(self, product_ids: list[int]) -> list[ProductChannelPublicationEntity]:
        """Get all publications of given products"""
        publications = self.get_queryset().filter(product_id__in=product_ids)
        return await self.to_entities(self.base_entity_class, publications)
