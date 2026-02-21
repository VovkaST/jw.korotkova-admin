from __future__ import annotations

from root.apps.bot import bot_config
from root.apps.bot.dtos import BotDTO
from root.apps.bot.repositories import BotRepository
from root.contrib.clean_architecture.utils import create_dto_object


class BotSettingsService:
    bot_repo = BotRepository()

    async def get_bot(self, bot_name: str) -> BotDTO:
        """Return bot data as DTO for API boundary."""
        instance = await self.bot_repo.get_bot(bot_name)
        if instance is None:
            return BotDTO(
                name=None,
                version=None,
                description=None,
                welcome_message=None,
            )
        return await create_dto_object(BotDTO, instance)

    async def get_description(self, bot_name: str) -> str | None:
        instance = await self.bot_repo.get_bot(bot_name)
        return instance.description if instance else None

    async def get_version(self, bot_name: str) -> str:
        instance = await self.bot_repo.get_bot(bot_name)
        if not instance:
            return bot_config.DEFAULT_VERSION
        return instance.version
