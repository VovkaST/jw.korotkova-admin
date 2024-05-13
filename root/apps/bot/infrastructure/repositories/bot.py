from __future__ import annotations

from typing import TYPE_CHECKING

from root.apps.bot.application.boundaries.bot import IBotRepository
from root.apps.bot.application.domain.entities import BotEntity
from root.apps.bot.models import Bot
from root.contrib.clean_architecture.utils import create_entity_object

if TYPE_CHECKING:
    pass


class BotRepository(IBotRepository):
    model = Bot

    async def get_bot(self, bot_name: str) -> BotEntity | None:
        try:
            instance = await self.model.objects.aget(name=bot_name)
        except self.model.DoesNotExist:
            return
        return create_entity_object(BotEntity, instance)
