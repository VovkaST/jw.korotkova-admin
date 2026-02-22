import pytest

from root.apps.products.application.interactors import ProductInteractor

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


class TestProductInteractor:
    async def test_get_products_in_stock_empty(self):
        interactor = ProductInteractor()
        result = await interactor.get_products_in_stock()
        assert result == []

    async def test_get_products_in_stock_filters_by_in_stock(self, test_product_type, test_product):
        async with (
            test_product_type(name="T") as ptype,
            test_product(ptype, title="A", in_stock=True),
            test_product(ptype, title="B", in_stock=False),
        ):
            interactor = ProductInteractor()
            result = await interactor.get_products_in_stock()
        assert len(result) == 1
        assert result[0].title == "A"
