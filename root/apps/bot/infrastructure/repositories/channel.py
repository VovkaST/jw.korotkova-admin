from __future__ import annotations

from root.apps.bot.application.boundaries import IChannelRepository
from root.apps.bot.application.domain.entities import ChannelEntity
from root.apps.bot.models import Channel
from root.base.repository import BaseRepository
from root.core.errors import InterceptError


class ChannelRepository(BaseRepository, IChannelRepository):
    model = Channel
    base_entity_class = ChannelEntity

    @InterceptError.allow_does_not_exists
    async def get_by_channel_id(self, channel_id: int) -> base_entity_class:
        queryset = self.get_queryset()
        channel = await queryset.aget(chat_id=channel_id)
        return await self.to_entity(self.base_entity_class, channel)
