from __future__ import annotations

from root.apps.products.application.boundaries.product import IProductRepository
from root.apps.products.application.domain.entities import ProductEntity
from root.apps.products.models import Product
from root.base.repository import BaseRepository
from root.contrib.clean_architecture.interfaces import ObjectId


class ProductRepository(BaseRepository, IProductRepository):
    model = Product
    base_entity_class = ProductEntity

    async def get_products(self, product_ids: list[ObjectId]) -> list[base_entity_class]:
        """Get all given products"""
        publications = self.get_queryset().filter(id__in=product_ids)
        return await self.to_entities(self.base_entity_class, publications)
