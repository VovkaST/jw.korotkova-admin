from __future__ import annotations

from root.apps.bot.models import Channel
from root.base.repository import BaseRepository
from root.core.errors import InterceptError


class ChannelRepository(BaseRepository):
    model = Channel

    @InterceptError.allow_does_not_exists
    async def get(self, pk: int) -> Channel | None:
        return await self.get_queryset().aget(pk=pk)

    @InterceptError.allow_does_not_exists
    async def get_by_channel_id(self, channel_id: int) -> Channel | None:
        return await self.get_queryset().aget(chat_id=channel_id)

    async def create(
        self,
        *,
        chat_id: int,
        title: str,
        link: str | None = None,
    ) -> Channel:
        return await self.model.objects.acreate(
            chat_id=chat_id, title=title, link=link
        )
