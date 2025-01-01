from __future__ import annotations

from abc import ABC, abstractmethod

from root.apps.products.application.domain.entities import ProductChannelPublicationEntity


class IProductChannelPublicationRepository(ABC):
    @abstractmethod
    async def get_product_publications(self, product_id: int) -> list[ProductChannelPublicationEntity]:
        """Get all product publications"""

    @abstractmethod
    async def get_products_publications(self, product_ids: list[int]) -> list[ProductChannelPublicationEntity]:
        """Get all publications of given products"""
