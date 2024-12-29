from __future__ import annotations

from root.apps.bot.application.domain.enums import ComparisonType
from root.apps.bot.infrastructure.repositories.user_chats import UserChatRepository


class UserChatInteractor:
    user_chats_repo = UserChatRepository()

    async def get_chat(
        self, *, user_id: str = None, username: str = None, comparison: ComparisonType = ComparisonType.OR
    ) -> str:
        """Get stored chat id by user id"""
        return await self.user_chats_repo.get_chat(user_id=user_id, username=username, comparison=comparison)

    async def create_user_chat(self, user_id: str, chat_id: str | int, username: str = None) -> None:
        """Create user chat"""
        return await self.user_chats_repo.create(user_id=user_id, chat_id=chat_id, username=username)
