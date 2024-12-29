from __future__ import annotations

from django.db.models import Q

from root.apps.bot.application.boundaries.user_chats import IUserChatRepository
from root.apps.bot.application.domain.entities import UserChatEntity
from root.apps.bot.application.domain.enums import ComparisonType
from root.apps.bot.models import UserChat
from root.base.repository import BaseRepository
from root.core.errors import InterceptError


class UserChatRepository(BaseRepository, IUserChatRepository):
    model = UserChat
    base_entity_class = UserChatEntity

    @InterceptError.allow_does_not_exists
    async def get_chat(
        self, *, user_id: str | int = None, username: str = None, comparison: ComparisonType = ComparisonType.OR
    ) -> str:
        assert user_id or username, "user_id or username is required"

        if user_id and not username:
            instance = await self.model.objects.aget(user_id=user_id)

        elif not user_id and username:
            instance = await self.model.objects.aget(username=username)

        else:
            if comparison == ComparisonType.AND:
                instance = await self.model.objects.aget(user_id=user_id, username=username)
            else:
                instance = await self.model.objects.aget(Q(user_id=user_id) | Q(username=username))

        return instance.chat_id

    @InterceptError.allow_does_not_exists
    async def create(self, user_id: str | int, chat_id: str, username: str = None) -> base_entity_class:
        if username and not username.startswith("@"):
            username = f"@{username}"
        return await super().create(user_id=str(user_id), username=username, chat_id=str(chat_id))
