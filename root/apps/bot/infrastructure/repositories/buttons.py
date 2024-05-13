from __future__ import annotations

from root.apps.bot.application.boundaries.buttons import IButtonsRepository
from root.apps.bot.application.domain.entities import ButtonEntity
from root.apps.bot.models import Buttons
from root.contrib.clean_architecture.utils import create_entity_object


class ButtonsRepository(IButtonsRepository):
    model = Buttons

    async def get_bot_buttons(self, bot_name: str) -> list[ButtonEntity]:
        qs = self.model.objects.filter(bot__name=bot_name)
        return [create_entity_object(ButtonEntity, instance) async for instance in qs.aiterator()]

    async def get_button_by_text(self, bot_name: str, text: str) -> ButtonEntity | None:
        try:
            instance = await self.model.objects.aget(bot__name=bot_name, text=text)
            return create_entity_object(ButtonEntity, instance)
        except self.model.DoesNotExist:
            pass
