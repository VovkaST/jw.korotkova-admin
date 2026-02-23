import pytest

from root.apps.products.services import ProductService

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


class TestProductViewSet:
    """Tests for get_products_in_stock (used by API)."""

    async def test_get_products_in_stock_empty(self):
        service = ProductService()
        result = await service.get_products_in_stock_dto()
        assert result == []

    async def test_get_products_in_stock_returns_only_in_stock(self, test_product_type, test_product):
        async with (
            test_product_type(name="Type A") as ptype,
            test_product(ptype, title="In stock", in_stock=True),
            test_product(ptype, title="Out of stock", in_stock=False),
        ):
            service = ProductService()
            result = await service.get_products_in_stock_dto()
        assert len(result) == 1
        assert result[0].title == "In stock"
        assert result[0].in_stock is True

    async def test_get_products_in_stock_returns_dtos_with_expected_fields(self, test_product_type, test_product):
        async with (
            test_product_type(name="Type A") as ptype,
            test_product(ptype, title="Product 1", description="Desc", price="50.00"),
        ):
            service = ProductService()
            result = await service.get_products_in_stock_dto()
        assert len(result) == 1
        dto = result[0]
        assert dto.title == "Product 1"
        assert dto.description == "Desc"
        assert float(dto.price) == 50.0
        assert dto.type.name == "Type A"
        assert dto.guid is not None
        assert dto.files == []
