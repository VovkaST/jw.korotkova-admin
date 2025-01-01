from __future__ import annotations

from abc import ABC

from root.apps.products.application.domain.entities import ProductEntity


class IProductRepository(ABC):
    async def get_products(self, product_ids: list[int]) -> list[ProductEntity]:
        """Get all given products"""
