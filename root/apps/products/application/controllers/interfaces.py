from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from root.apps.products.application.domain.entities import ProductEntity
from root.contrib.clean_architecture.interfaces import ObjectId


class IProductController(ABC):
    @abstractmethod
    async def get_products_in_stock(self) -> Sequence[ProductEntity]:
        """Get all products in stock"""

    @abstractmethod
    async def new_channel_post(self, channel_id: int, message: str):
        pass

    @abstractmethod
    async def add_images(self, product_id: ObjectId, files, description: str | None = None):
        pass


class IProductChannelPublicationController(ABC):
    @abstractmethod
    async def new_channel_post(self, channel_id: int, message_id: int, text: str):
        pass

    @abstractmethod
    async def edited_channel_post(self, channel_id: int, message_id: int, text: str):
        pass
