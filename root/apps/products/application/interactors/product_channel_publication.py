from __future__ import annotations

import re

from root.apps.bot.infrastructure.repositories import ChannelRepository
from root.apps.products.application.boundaries.dtos import ProductChannelPublicationCreateDTO
from root.apps.products.infrastrucure.repositories import ProductChannelPublicationRepository, ProductRepository

re_product_name = re.compile(r"Лот\s*#(\d+)", flags=re.IGNORECASE)


class ProductChannelPublicationInteractor:
    product_repo = ProductRepository()
    channel_repo = ChannelRepository()
    channel_publication_repo = ProductChannelPublicationRepository()

    async def new_channel_post(self, channel_id: int, message_id: int, text: str):
        matches = re_product_name.findall(text)
        if not matches:
            return
        channel = await self.channel_repo.get_by_channel_id(channel_id)
        product_ids = list(map(int, matches))
        actual_products = await self.product_repo.get_products(product_ids)
        publications = await self.channel_publication_repo.get_products_publications(product_ids)
        public_product_ids = {publication.product_id for publication in publications}
        for product in actual_products:
            create_dto = ProductChannelPublicationCreateDTO(
                product_id=product.id,
                channel_id=channel.id,
                message_id=message_id,
                text=text,
                is_main=product.id not in public_product_ids,
            )
            await self.channel_publication_repo.create(create_dto)
