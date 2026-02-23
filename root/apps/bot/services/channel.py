from __future__ import annotations

from root.apps.bot.models import Channel
from root.apps.bot.repositories import ChannelRepository


class ChannelService:
    channel_repo = ChannelRepository()

    async def get_channel(self, *, pk: int | None = None, channel_id: int | None = None) -> Channel | None:
        assert pk or channel_id, "You must provide either pk or channel_id"
        if pk:
            return await self.channel_repo.get(pk=pk)
        return await self.channel_repo.get_by_channel_id(channel_id=channel_id)

    async def create_channel(self, channel_id: int, title: str, link: str | None = None) -> None:
        await self.channel_repo.create(chat_id=channel_id, title=title, link=link)
