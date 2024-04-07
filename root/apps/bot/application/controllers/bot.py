from __future__ import annotations

from typing import TYPE_CHECKING

from root.apps.bot.application.controllers.interfaces import IBotController
from root.apps.bot.application.interactors.bot import BotInteractor

if TYPE_CHECKING:
    from root.apps.bot.application.boundaries.dtos import BotDTO


class BotController(IBotController):
    bot_interactor = BotInteractor()

    async def get_bot(self, bot_name: str) -> BotDTO:
        return await self.bot_interactor.get_bot(bot_name)

    async def get_bot_description(self, bot_name: str) -> str:
        return await self.bot_interactor.get_description(bot_name)

    async def get_bot_version(self, bot_name: str) -> str:
        return await self.bot_interactor.get_version(bot_name)
