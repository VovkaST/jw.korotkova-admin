from __future__ import annotations

from root.apps.products.application.controllers.interfaces import IProductController
from root.apps.products.application.interactors import ProductInteractor


class ProductController(IProductController):
    product_interactor = ProductInteractor()

    async def new_channel_post(self, channel_id: int, message: str):
        return await self.product_interactor.new_channel_post(channel_id, message)
