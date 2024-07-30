from __future__ import annotations

from root.apps.bot.application.boundaries.bot import IBotRepository
from root.apps.bot.application.domain.entities import BotEntity
from root.apps.bot.models import Bot
from root.base.repository import BaseRepository


class BotRepository(BaseRepository, IBotRepository):
    model = Bot

    async def get_bot(self, bot_name: str) -> BotEntity | None:
        try:
            instance = await self.model.objects.aget(name=bot_name)
        except self.model.DoesNotExist:
            return
        return await self.to_entity(BotEntity, instance)
