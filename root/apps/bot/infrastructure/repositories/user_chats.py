from __future__ import annotations

from root.apps.bot.application.boundaries.user_chats import IUserChatRepository
from root.apps.bot.models import UserChat
from root.base.repository import BaseRepository
from root.core.errors import InterceptError


class UserChatRepository(BaseRepository, IUserChatRepository):
    model = UserChat

    @InterceptError.allow_does_not_exists
    async def get_chat(self, user_id: str) -> str:
        instance = await self.model.objects.aget(user_id=user_id)
        return instance.chat_id
