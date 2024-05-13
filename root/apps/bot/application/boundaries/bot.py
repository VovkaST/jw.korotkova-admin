from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class IBotRepository(ABC):
    @abstractmethod
    async def get_bot(self, bot_name: str):
        pass
