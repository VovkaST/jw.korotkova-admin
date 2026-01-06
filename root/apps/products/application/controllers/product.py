from __future__ import annotations

from collections.abc import Sequence

from root.apps.products.application.boundaries.dtos import ProductFileCreateDTO
from root.apps.products.application.controllers.interfaces import IProductController
from root.apps.products.application.domain.entities import ProductEntity
from root.apps.products.application.interactors import ProductInteractor
from root.contrib.clean_architecture.interfaces import ObjectId


class ProductController(IProductController):
    product_interactor = ProductInteractor()

    async def get_products_in_stock(self) -> Sequence[ProductEntity]:
        return await self.product_interactor.get_products_in_stock()

    async def new_channel_post(self, channel_id: int, message: str):
        return await self.product_interactor.new_channel_post(channel_id, message)

    async def add_images(self, product_id: ObjectId, files: list[ProductFileCreateDTO]):
        return await self.product_interactor.add_images(product_id, files)
