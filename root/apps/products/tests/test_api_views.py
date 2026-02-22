import pytest

from root.apps.products.application.controllers import ProductController

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


class TestProductViewSet:
    """Tests for get_products_in_stock (used by API)."""

    async def test_get_products_in_stock_empty(self):
        controller = ProductController()
        result = await controller.get_products_in_stock()
        assert result == []

    async def test_get_products_in_stock_returns_only_in_stock(self, test_product_type, test_product):
        async with (
            test_product_type(name="Type A") as ptype,
            test_product(ptype, title="In stock", in_stock=True),
            test_product(ptype, title="Out of stock", in_stock=False),
        ):
            controller = ProductController()
            result = await controller.get_products_in_stock()
        assert len(result) == 1
        assert result[0].title == "In stock"
        assert result[0].in_stock is True

    async def test_get_products_in_stock_returns_entities_with_expected_fields(self, test_product_type, test_product):
        async with (
            test_product_type(name="Type A") as ptype,
            test_product(ptype, title="Product 1", description="Desc", price="50.00"),
        ):
            controller = ProductController()
            result = await controller.get_products_in_stock()
        assert len(result) == 1
        entity = result[0]
        assert entity.title == "Product 1"
        assert entity.description == "Desc"
        assert float(entity.price) == 50.0
        assert entity.type.name == "Type A"
        assert entity.guid is not None
        assert entity.files == []
