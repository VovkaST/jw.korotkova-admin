from __future__ import annotations

from root.apps.bot.exceptions import UnknownButton
from root.apps.bot.models import Buttons
from root.apps.bot.repositories import ButtonsRepository


class ButtonsService:
    buttons_repo = ButtonsRepository()

    async def get_buttons(self, bot_name: str) -> list[Buttons]:
        return await self.buttons_repo.get_bot_buttons(bot_name)

    async def get_button_answer(self, bot_name: str, button_text: str) -> str:
        button = await self.buttons_repo.get_button_by_text(bot_name, button_text)
        if not button:
            raise UnknownButton
        return button.simple_response
