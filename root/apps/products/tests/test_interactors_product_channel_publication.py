import pytest

from root.apps.products.application.interactors.product_channel_publication import (
    ProductChannelPublicationInteractor,
)
from root.apps.products.models import ProductChannelPublication

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


class TestExtractProductIds:
    async def test_extract_product_ids_empty(self):
        interactor = ProductChannelPublicationInteractor()
        result = await interactor.extract_product_ids("no lot here")
        assert result == []

    async def test_extract_product_ids_single(self):
        interactor = ProductChannelPublicationInteractor()
        result = await interactor.extract_product_ids("Лот #42")
        assert result == [42]

    async def test_extract_product_ids_multiple(self):
        interactor = ProductChannelPublicationInteractor()
        result = await interactor.extract_product_ids("Лот #1 и лот #22, лот #333")
        assert result == [1, 22, 333]

    async def test_extract_product_ids_case_insensitive(self):
        interactor = ProductChannelPublicationInteractor()
        result = await interactor.extract_product_ids("ЛОТ #7")
        assert result == [7]


class TestNewChannelPost:
    async def test_new_channel_post_no_lots_does_nothing(self, test_product_type, test_product, test_channel):
        async with (
            test_product_type() as ptype,
            test_product(ptype, title="P"),
            test_channel(chat_id=111) as channel,
        ):
            interactor = ProductChannelPublicationInteractor()
            await interactor.new_channel_post(channel_id=channel.chat_id, message_id=1, text="no lot mentioned")
        count = await ProductChannelPublication.objects.acount()
        assert count == 0

    async def test_new_channel_post_creates_publications(self, test_product_type, test_product, test_channel):
        async with (
            test_product_type() as ptype,
            test_product(ptype, title="P1") as product,
            test_channel(chat_id=222) as channel,
        ):
            interactor = ProductChannelPublicationInteractor()
            await interactor.new_channel_post(channel_id=channel.chat_id, message_id=10, text=f"Лот #{product.id}")
            count = await ProductChannelPublication.objects.filter(channel=channel, message_id=10).acount()
            assert count == 1
            pub = await ProductChannelPublication.objects.aget(channel=channel, message_id=10)
            assert pub.product_id == product.id
            assert pub.text == f"Лот #{product.id}"
            assert pub.is_main is True

    async def test_new_channel_post_ignores_nonexistent_lot_ids(self, test_product_type, test_product, test_channel):
        async with (
            test_product_type() as ptype,
            test_product(ptype, title="P1") as product,
            test_channel(chat_id=333) as channel,
        ):
            interactor = ProductChannelPublicationInteractor()
            # 99999 does not exist
            await interactor.new_channel_post(
                channel_id=channel.chat_id, message_id=20, text=f"Лот #{product.id} и Лот #99999"
            )
            count = await ProductChannelPublication.objects.filter(channel=channel, message_id=20).acount()
            assert count == 1


class TestEditedChannelPost:
    async def test_edited_channel_post_updates_text(self, test_product_type, test_product, test_channel):
        async with (
            test_product_type() as ptype,
            test_product(ptype, title="P1") as product,
            test_channel(chat_id=444) as channel,
        ):
            pub = await ProductChannelPublication.objects.acreate(
                product=product, channel=channel, message_id=30, text="old text", is_main=True
            )
            interactor = ProductChannelPublicationInteractor()
            await interactor.edited_channel_post(
                channel_id=channel.chat_id, message_id=30, text=f"Лот #{product.id} new text"
            )
            await pub.arefresh_from_db()
            assert pub.text == f"Лот #{product.id} new text"
