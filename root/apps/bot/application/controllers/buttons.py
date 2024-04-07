from __future__ import annotations

from typing import TYPE_CHECKING

from root.apps.bot.application.controllers.interfaces import IButtonsController
from root.apps.bot.application.interactors.buttons import ButtonsInteractor

if TYPE_CHECKING:
    from root.apps.bot.application.boundaries.dtos import ButtonDTO


class ButtonsController(IButtonsController):
    buttons_interactor = ButtonsInteractor()

    async def get_buttons(self, bot_name: str) -> list[ButtonDTO]:
        return await self.buttons_interactor.get_bot_buttons(bot_name)

    async def get_button_simple_response(self, bot_name: str, button_text: str) -> str | None:
        return await self.buttons_interactor.get_button_answer(bot_name, button_text)
