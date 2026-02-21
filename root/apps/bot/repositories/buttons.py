from __future__ import annotations

from root.apps.bot.models import Buttons
from root.base.repository import BaseRepository
from root.core.errors import InterceptError


class ButtonsRepository(BaseRepository):
    model = Buttons

    async def get_bot_buttons(self, bot_name: str) -> list[Buttons]:
        qs = self.model.objects.filter(bot__name=bot_name)
        return [inst async for inst in qs.aiterator()]

    @InterceptError.allow_does_not_exists
    async def get_button_by_text(self, bot_name: str, text: str) -> Buttons | None:
        return await self.model.objects.aget(bot__name=bot_name, text=text)
