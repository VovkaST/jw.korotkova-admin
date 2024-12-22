from __future__ import annotations

from root.apps.bot.application.boundaries.bot import IBotRepository
from root.apps.bot.application.domain.entities import BotEntity
from root.apps.bot.models import Bot
from root.base.repository import BaseRepository
from root.core.errors import InterceptError


class BotRepository(BaseRepository, IBotRepository):
    model = Bot

    @InterceptError.allow_does_not_exists
    async def get_bot(self, bot_name: str) -> BotEntity | None:
        instance = await self.model.objects.aget(name=bot_name)
        return await self.to_entity(BotEntity, instance)
