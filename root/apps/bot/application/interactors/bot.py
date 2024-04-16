from __future__ import annotations

from root.apps.bot import bot_config
from root.apps.bot.application.boundaries.dtos import BotDTO
from root.apps.bot.infrastructure.repositories.bot import BotRepository
from root.contrib.clean_architecture.utils import create_dto_object


class BotInteractor:
    bot_repo = BotRepository()

    async def get_bot(self, bot_name: str) -> BotDTO:
        entity = await self.bot_repo.get_bot(bot_name)
        return await create_dto_object(BotDTO, entity)

    async def get_description(self, bot_name: str) -> str:
        entity = await self.bot_repo.get_bot(bot_name)
        if entity:
            return entity.description

    async def get_version(self, bot_name: str) -> str:
        entity = await self.bot_repo.get_bot(bot_name)
        if not entity:
            return bot_config.DEFAULT_VERSION
        return entity.version
