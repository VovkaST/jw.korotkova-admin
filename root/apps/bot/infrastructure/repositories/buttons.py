from __future__ import annotations

from root.apps.bot.application.boundaries.buttons import IButtonsRepository
from root.apps.bot.application.domain.entities import ButtonEntity
from root.apps.bot.models import Buttons
from root.base.repository import BaseRepository
from root.core.errors import InterceptError


class ButtonsRepository(BaseRepository, IButtonsRepository):
    model = Buttons

    async def get_bot_buttons(self, bot_name: str) -> list[ButtonEntity]:
        qs = self.model.objects.filter(bot__name=bot_name)
        return await self.to_entities(ButtonEntity, qs)

    @InterceptError.allow_does_not_exists
    async def get_button_by_text(self, bot_name: str, text: str) -> ButtonEntity | None:
        instance = await self.model.objects.aget(bot__name=bot_name, text=text)
        return await self.to_entity(ButtonEntity, instance)
