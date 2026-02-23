from __future__ import annotations

from django.db.models import Q

from root.apps.bot.enums import ComparisonType
from root.apps.bot.models import UserChat
from root.base.repository import BaseRepository
from root.core.errors import InterceptError


class UserChatRepository(BaseRepository[UserChat]):
    model = UserChat

    @InterceptError.allow_does_not_exists
    async def get_chat(
        self,
        *,
        user_id: str | int | None = None,
        username: str | None = None,
        comparison: ComparisonType = ComparisonType.OR,
    ) -> str | None:
        assert user_id or username, "user_id or username is required"

        if user_id and not username:
            query = Q(user_id=user_id)
        elif not user_id and username:
            query = Q(username=username)
        else:
            if comparison == ComparisonType.AND:
                query = Q(user_id=user_id, username=username)
            else:
                query = Q(user_id=user_id) | Q(username=username)

        instance = await self.objects.aget(query)
        return instance.chat_id

    async def create(
        self,
        *,
        user_id: str | int,
        chat_id: str | int,
        username: str | None = None,
    ) -> UserChat:
        if username and not username.startswith("@"):
            username = f"@{username}"
        return await self.objects.acreate(user_id=str(user_id), chat_id=str(chat_id), username=username)
