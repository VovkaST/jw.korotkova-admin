from __future__ import annotations

from root.apps.bot.application.controllers.interfaces import IChannelController
from root.apps.bot.application.interactors import ChannelInteractor


class ChannelController(IChannelController):
    channel_interactor = ChannelInteractor()

    async def get_channel(self, channel_id: int) -> int:
        return await self.channel_interactor.get_channel(channel_id=channel_id)

    async def create_channel(self, channel_id: int, title: str) -> None:
        return await self.channel_interactor.create_channel(channel_id=channel_id, title=title)
