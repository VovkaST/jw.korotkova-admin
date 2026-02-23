from __future__ import annotations

from django.conf import settings

from root.apps.products.dtos import (
    ProductDTO,
    ProductFileCreateDTO,
    ProductFileDTO,
    ProductTypeDTO,
)
from root.apps.products.models import Product
from root.apps.products.repositories import ProductRepository
from root.base.entity import ImageMeta
from root.contrib.clean_architecture.interfaces import ObjectId
from root.core.utils import Singleton


def _product_to_dto(product: Product) -> ProductDTO:
    type_dto = ProductTypeDTO(
        id=product.type_id or 0,
        name=product.type.name if product.type else "",
        description=product.type.description if product.type else None,
        is_active=product.type.is_active if product.type else True,
    )
    files_dto = []
    for f in product.files.all():
        meta = ImageMeta(**(f.meta or {}))
        files_dto.append(
            ProductFileDTO(
                id=f.pk,
                file=f.file.url if f.file else "",
                description=f.description,
                meta=meta,
            )
        )
    return ProductDTO(
        guid=product.guid,
        type=type_dto,
        type_id=product.type_id or 0,
        title=product.title,
        description=product.description,
        price=product.price,
        in_stock=product.in_stock,
        files=files_dto,
    )


class ProductService(Singleton):
    product_repo = ProductRepository()

    def get_products_in_stock(self):
        return self.product_repo.get_products_in_stock()

    async def get_products_in_stock_dto(self) -> list[ProductDTO]:
        qs = self.get_products_in_stock()
        return [_product_to_dto(p) async for p in qs]

    async def add_images(
        self,
        product_id: ObjectId,
        files: list[ProductFileCreateDTO],
    ):
        return await self.product_repo.add_images(product_id, files, sizes=settings.THUMBNAIL_SIZES)
