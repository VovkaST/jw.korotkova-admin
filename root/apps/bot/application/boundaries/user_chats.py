from __future__ import annotations

from abc import ABC, abstractmethod

from root.apps.bot.application.domain.enums import ComparisonType


class IUserChatRepository(ABC):
    @abstractmethod
    async def get_chat(
        self, *, user_id: str = None, username: str = None, comparison: ComparisonType = ComparisonType.OR
    ) -> str:
        """Get stored chat id by user id"""
