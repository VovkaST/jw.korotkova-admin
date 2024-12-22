from __future__ import annotations

from abc import ABC, abstractmethod


class IUserChatRepository(ABC):
    @abstractmethod
    async def get_chat(self, user_id: str) -> str:
        """Get stored chat id by user id"""
