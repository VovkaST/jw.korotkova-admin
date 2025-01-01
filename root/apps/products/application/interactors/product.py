from __future__ import annotations

from root.apps.bot.infrastructure.repositories import ChannelRepository
from root.apps.products.infrastrucure.repositories import ProductRepository


class ProductInteractor:
    product_repo = ProductRepository()
    channel_repo = ChannelRepository()

    async def new_channel_post(self, channel_id: int, message: str):
        match = re_product_name.findall(message)
        for product_id in match:
            product = await self.product_repo.get(pk=product_id)
            if product:
                await self.product_repo.update(product, is_active=True)
