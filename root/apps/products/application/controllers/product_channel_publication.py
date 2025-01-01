from __future__ import annotations

from root.apps.products.application.controllers.interfaces import IProductChannelPublicationController
from root.apps.products.application.interactors import ProductChannelPublicationInteractor


class ProductChannelPublicationController(IProductChannelPublicationController):
    channel_publication_interactor = ProductChannelPublicationInteractor()

    async def new_channel_post(self, channel_id: int, message_id: int, text: str):
        return await self.channel_publication_interactor.new_channel_post(channel_id, message_id, text)
