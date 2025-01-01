from __future__ import annotations

from abc import ABC, abstractmethod


class IProductController(ABC):
    @abstractmethod
    async def new_channel_post(self, channel_id: int, message: str):
        pass


class IProductChannelPublicationController(ABC):
    @abstractmethod
    async def new_channel_post(self, channel_id: int, message_id: int, text: str):
        pass
