from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from root.apps.bot.application.domain.entities import ButtonEntity


class IButtonsRepository(ABC):
    @abstractmethod
    async def get_bot_buttons(self, bot_name: str) -> list[ButtonEntity]:
        pass

    @abstractmethod
    async def get_button_by_text(self, bot_name: str, text: str) -> ButtonEntity | None:
        pass
