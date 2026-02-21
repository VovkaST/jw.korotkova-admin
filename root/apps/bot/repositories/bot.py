from __future__ import annotations

from root.apps.bot.models import Bot
from root.base.repository import BaseRepository
from root.core.errors import InterceptError


class BotRepository(BaseRepository):
    model = Bot

    @InterceptError.allow_does_not_exists
    async def get_bot(self, bot_name: str) -> Bot | None:
        return await self.model.objects.aget(name=bot_name)
