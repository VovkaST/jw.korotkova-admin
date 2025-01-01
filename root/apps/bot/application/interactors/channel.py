from __future__ import annotations

from root.apps.bot.infrastructure.repositories import ChannelRepository


class ChannelInteractor:
    channel_repo = ChannelRepository()

    async def get_channel(self, *, pk: int = None, channel_id: int = None) -> int:
        assert pk or channel_id, "You must provide either pk or channel_id"
        if pk:
            return await self.channel_repo.get(pk=pk)
        if channel_id:
            return await self.channel_repo.get_by_channel_id(channel_id=channel_id)

    async def create_channel(self, channel_id: int, title: str) -> None:
        return await self.channel_repo.create(chat_id=channel_id, title=title)
