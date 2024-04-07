from abc import ABC, abstractmethod

from root.apps.bot.application.boundaries.dtos import ButtonDTO


class IBotController(ABC):
    @abstractmethod
    async def get_bot(self, bot_name: str) -> list:
        pass

    @abstractmethod
    async def get_bot_description(self, bot_name: str) -> str:
        pass

    @abstractmethod
    async def get_bot_version(self, bot_name: str) -> str:
        pass


class IButtonsController(ABC):
    @abstractmethod
    async def get_buttons(self, bot_name: str) -> list[ButtonDTO]:
        pass

    @abstractmethod
    async def get_button_simple_response(self, bot_name: str, button_text: str) -> str | None:
        pass
