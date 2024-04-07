from __future__ import annotations

from root.apps.bot.application.boundaries.dtos import ButtonDTO
from root.apps.bot.application.domain.exceptions import UnknownButton
from root.apps.bot.infrastructure.repositories.buttons import ButtonsRepository
from root.contrib.clean_architecture.utils import create_dto_object


class ButtonsInteractor:
    buttons_repo = ButtonsRepository()

    async def get_bot_buttons(self, bot_name: str) -> list[ButtonDTO]:
        entities = await self.buttons_repo.get_bot_buttons(bot_name)
        return [await create_dto_object(ButtonDTO, entity) for entity in entities]

    async def get_button_answer(self, bot_name: str, button_text: str) -> str:
        button = await self.buttons_repo.get_button_by_text(bot_name, button_text)
        if not button:
            raise UnknownButton
        return button.simple_response
