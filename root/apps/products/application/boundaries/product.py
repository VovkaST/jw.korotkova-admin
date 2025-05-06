from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from root.contrib.clean_architecture.interfaces import ObjectId

if TYPE_CHECKING:
    from root.apps.products.application.domain.entities import ProductEntity


class IProductRepository(ABC):
    @abstractmethod
    async def get_products(self, product_ids: list[ObjectId]) -> list[ProductEntity]:
        """Get all given products"""

    @abstractmethod
    async def get_products_in_stock(self):
        """Get all products in stock"""
