"""Fixtures for products app tests."""

from collections.abc import Callable

import pytest

from root.apps.bot.models import Channel
from root.apps.products.enums import ProductCategoryChoices
from root.apps.products.models import Product, ProductChannelPublication, ProductType
from root.core.utils import removable


@pytest.fixture
def test_product_type() -> Callable:
    @removable
    async def _wrapper(name: str = "Test type", description: str | None = None, is_active: bool = True) -> ProductType:
        instance = await ProductType.objects.acreate(name=name, description=description, is_active=is_active)
        return instance

    return _wrapper


@pytest.fixture
def test_product() -> Callable:
    @removable
    async def _wrapper(
        product_type: ProductType,
        title: str = "Test product",
        description: str = "Description",
        price: str = "100.00",
        in_stock: bool = True,
        category: str = ProductCategoryChoices.PRODUCT,
    ) -> Product:
        instance = await Product.objects.acreate(
            type=product_type, title=title, description=description, price=price, in_stock=in_stock, category=category
        )
        return instance

    return _wrapper


@pytest.fixture
def test_channel() -> Callable:
    @removable
    async def _wrapper(chat_id: int = -1001234567890, title: str = "Test channel", link: str | None = None) -> Channel:
        instance = await Channel.objects.acreate(chat_id=chat_id, title=title, link=link)
        return instance

    return _wrapper


@pytest.fixture
def test_product_channel_publication() -> Callable:
    @removable
    async def _wrapper(
        product: Product, channel: Channel, message_id: int = 1, text: str = "Лот #1", is_main: bool = True
    ) -> ProductChannelPublication:
        instance = await ProductChannelPublication.objects.acreate(
            product=product, channel=channel, message_id=message_id, text=text, is_main=is_main
        )
        return instance

    return _wrapper
