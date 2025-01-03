from __future__ import annotations

import re
from collections import defaultdict

from root.apps.bot.infrastructure.repositories import ChannelRepository
from root.apps.products.application.boundaries.dtos import (
    ProductChannelPublicationCreateDTO,
    ProductChannelPublicationUpdateDTO,
)
from root.apps.products.application.domain.entities import ProductChannelPublicationEntity
from root.apps.products.infrastrucure.repositories import ProductChannelPublicationRepository, ProductRepository


class ProductChannelPublicationInteractor:
    RE_PRODUCT_NAME = re.compile(r"Лот\s*#(\d+)", flags=re.IGNORECASE)

    product_repo = ProductRepository()
    channel_repo = ChannelRepository()
    channel_publication_repo = ProductChannelPublicationRepository()

    async def extract_product_ids(self, text: str) -> list[int]:
        matches = self.RE_PRODUCT_NAME.findall(text)
        if not matches:
            return []
        return list(map(int, matches))

    async def new_channel_post(self, channel_id: int, message_id: int, text: str):
        product_ids = await self.extract_product_ids(text)
        if not product_ids:
            return
        channel = await self.channel_repo.get_by_channel_id(channel_id)
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

    async def edited_channel_post(self, channel_id: int, message_id: int, text: str):
        product_ids = await self.extract_product_ids(text)
        if not product_ids:
            return
        channel = await self.channel_repo.get_by_channel_id(channel_id)
        actual_products = await self.product_repo.get_products(product_ids)

        publications = await self.channel_publication_repo.get_products_publications(product_ids)
        products_publications: dict[int, list[int]] = defaultdict(list)
        for publication in publications:
            products_publications[publication.product_id].append(publication.message_id)

        existed_mentions = await self.channel_publication_repo.get_message_mentions(message_id)
        existed_product_mentions, existed_product_map = set(), {}
        for mention in existed_mentions:
            existed_product_mentions.add(mention.product_id)
            existed_product_map[mention.product_id] = mention
        message_mentioned_products = {p.id for p in actual_products}
        to_create_products_publications = message_mentioned_products - existed_product_mentions
        to_delete_products_publications = existed_product_mentions - message_mentioned_products
        to_update_products_publications = existed_product_mentions.intersection(message_mentioned_products)

        for product_id in to_create_products_publications:
            create_dto = ProductChannelPublicationCreateDTO(
                product_id=product_id,
                channel_id=channel.id,
                message_id=message_id,
                text=text,
                is_main=message_id in products_publications.get(product_id, []),
            )
            await self.channel_publication_repo.create(create_dto)

        for product_id in to_update_products_publications:
            publication = existed_product_map[product_id]
            product_publications = products_publications.get(product_id, [])
            publication_quantity = len(product_publications)
            update_dto = ProductChannelPublicationUpdateDTO(text=text)
            if not publication.is_main:
                update_dto.is_main = any(
                    [
                        not publication_quantity,
                        publication_quantity == 1 and message_id in product_publications,
                    ]
                )
            await self.channel_publication_repo.update(pk=publication.id, dto=update_dto)

        if to_delete_products_publications:
            await self.channel_publication_repo.delete(
                channel_id=channel.id, message_id=message_id, product_ids=to_delete_products_publications
            )
            publications_to_review = await self.channel_publication_repo.get_products_publications(
                to_delete_products_publications, order_by=["id"]
            )
            products_publications: dict[int, list[ProductChannelPublicationEntity]] = defaultdict(list)
            for publication in publications_to_review:
                products_publications[publication.product_id].append(publication)

            for product_id, publications in products_publications.items():
                if not publications:
                    continue
                first_publication = publications[0]
                if len(publications) == 1 and first_publication.is_main:
                    continue
                update_dto = ProductChannelPublicationUpdateDTO()
                update_dto.is_main = not any(p.is_main for p in publications)
                await self.channel_publication_repo.update(pk=first_publication.id, dto=update_dto)
