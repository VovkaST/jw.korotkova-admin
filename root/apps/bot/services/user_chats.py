from __future__ import annotations

from root.apps.bot.enums import ComparisonType
from root.apps.bot.repositories import UserChatRepository


class UserChatsService:
    user_chats_repo = UserChatRepository()

    async def get_chat(
        self,
        *,
        user_id: str | int | None = None,
        username: str | None = None,
        comparison: ComparisonType = ComparisonType.OR,
    ) -> str | None:
        return await self.user_chats_repo.get_chat(user_id=user_id, username=username, comparison=comparison)

    async def create_user_chat(
        self,
        user_id: str | int,
        chat_id: str | int,
        username: str | None = None,
    ) -> None:
        await self.user_chats_repo.create(user_id=user_id, chat_id=chat_id, username=username)
