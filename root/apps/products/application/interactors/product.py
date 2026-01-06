from __future__ import annotations

from django.conf import settings

from root.apps.products.application.boundaries.dtos import ProductFileCreateDTO
from root.apps.products.infrastructure.repositories import ProductFilesRepository, ProductRepository
from root.contrib.clean_architecture.interfaces import ObjectId


class ProductInteractor:
    product_repo = ProductRepository()
    product_files_repo = ProductFilesRepository()

    async def get_products_in_stock(self):
        return await self.product_repo.get_products_in_stock()

    async def add_images(self, product_id: ObjectId, files: list[ProductFileCreateDTO]):
        return await self.product_repo.add_images(product_id, files, sizes=settings.THUMBNAIL_SIZES)
