import pytest

from root.apps.products.services import ProductService

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


class TestProductService:
    async def test_get_products_in_stock_empty(self):
        service = ProductService()
        result = await service.get_products_in_stock_dto()
        assert result == []

    async def test_get_products_in_stock_filters_by_in_stock(self, test_product_type, test_product):
        async with (
            test_product_type(name="T") as ptype,
            test_product(ptype, title="A", in_stock=True),
            test_product(ptype, title="B", in_stock=False),
        ):
            service = ProductService()
            result = await service.get_products_in_stock_dto()
        assert len(result) == 1
        assert result[0].title == "A"
