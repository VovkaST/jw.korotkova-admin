from __future__ import annotations

from root.apps.products.infrastrucure.repositories import ProductRepository


class ProductInteractor:
    product_repo = ProductRepository()

    async def get_products_in_stock(self):
        return await self.product_repo.get_products_in_stock()
