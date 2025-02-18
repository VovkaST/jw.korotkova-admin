from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from root.apps.products.application.domain.entities import ProductChannelPublicationEntity


class IProductChannelPublicationRepository(ABC):
    @abstractmethod
    async def get_product_publications(self, product_id: int) -> list[ProductChannelPublicationEntity]:
        """Get all product publications"""

    @abstractmethod
    async def get_products_publications(
        self, product_ids: Iterable[int], order_by: list[str] = None
    ) -> list[ProductChannelPublicationEntity]:
        """Get all publications of given products"""

    @abstractmethod
    async def get_message_mentions(self, message_id: int) -> list[ProductChannelPublicationEntity]:
        """Get all publications mentions in given message"""
