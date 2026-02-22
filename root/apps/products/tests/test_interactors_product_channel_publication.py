import pytest

from root.apps.products.models import ProductChannelPublication
from root.apps.products.services import ProductChannelPublicationService

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


class TestExtractProductIds:
    async def test_extract_product_ids_empty(self):
        service = ProductChannelPublicationService()
        result = await service.extract_product_ids("no lot here")
        assert result == []

    async def test_extract_product_ids_single(self):
        service = ProductChannelPublicationService()
        result = await service.extract_product_ids("Лот #42")
        assert result == [42]

    async def test_extract_product_ids_multiple(self):
        service = ProductChannelPublicationService()
        result = await service.extract_product_ids("Лот #1 и лот #22, лот #333")
        assert result == [1, 22, 333]

    async def test_extract_product_ids_case_insensitive(self):
        service = ProductChannelPublicationService()
        result = await service.extract_product_ids("ЛОТ #7")
        assert result == [7]


class TestNewChannelPost:
    async def test_new_channel_post_no_lots_does_nothing(self, test_product_type, test_product, test_channel):
        async with (
            test_product_type() as ptype,
            test_product(ptype, title="P"),
            test_channel(chat_id=111) as channel,
        ):
            service = ProductChannelPublicationService()
            await service.new_channel_post(channel_id=channel.chat_id, message_id=1, text="no lot mentioned")
        count = await ProductChannelPublication.objects.acount()
        assert count == 0

    async def test_new_channel_post_creates_publications(self, test_product_type, test_product, test_channel):
        async with (
            test_product_type() as ptype,
            test_product(ptype, title="P1") as product,
            test_channel(chat_id=222) as channel,
        ):
            service = ProductChannelPublicationService()
            await service.new_channel_post(channel_id=channel.chat_id, message_id=10, text=f"Лот #{product.id}")
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
            service = ProductChannelPublicationService()
            # 99999 does not exist
            await service.new_channel_post(
                channel_id=channel.chat_id, message_id=20, text=f"Лот #{product.id} и Лот #99999"
            )
            count = await ProductChannelPublication.objects.filter(channel=channel, message_id=20).acount()
            assert count == 1

    async def test_new_channel_post_second_mention_is_not_main(self, test_product_type, test_product, test_channel):
        """When product already has a publication, new one in another message gets is_main=False."""
        async with (
            test_product_type() as ptype,
            test_product(ptype, title="P1") as product,
            test_channel(chat_id=334) as channel,
        ):
            await ProductChannelPublication.objects.acreate(
                product=product, channel=channel, message_id=21, text=f"Лот #{product.id}", is_main=True
            )
            service = ProductChannelPublicationService()
            await service.new_channel_post(channel_id=channel.chat_id, message_id=22, text=f"Лот #{product.id}")
            pub22 = await ProductChannelPublication.objects.aget(channel=channel, message_id=22)
            assert pub22.product_id == product.id
            assert pub22.is_main is False


class TestEditedChannelPost:
    async def test_edited_channel_post_no_lots_does_nothing(self, test_product_type, test_product, test_channel):
        async with (
            test_product_type() as ptype,
            test_product(ptype, title="P1") as product,
            test_channel(chat_id=440) as channel,
        ):
            pub = await ProductChannelPublication.objects.acreate(
                product=product, channel=channel, message_id=30, text="old", is_main=True
            )
            service = ProductChannelPublicationService()
            await service.edited_channel_post(channel_id=channel.chat_id, message_id=30, text="no lot in text")
            await pub.arefresh_from_db()
            assert pub.text == "old"

    async def test_edited_channel_post_updates_text(self, test_product_type, test_product, test_channel):
        async with (
            test_product_type() as ptype,
            test_product(ptype, title="P1") as product,
            test_channel(chat_id=444) as channel,
        ):
            pub = await ProductChannelPublication.objects.acreate(
                product=product, channel=channel, message_id=30, text="old text", is_main=True
            )
            service = ProductChannelPublicationService()
            await service.edited_channel_post(
                channel_id=channel.chat_id, message_id=30, text=f"Лот #{product.id} new text"
            )
            await pub.arefresh_from_db()
            assert pub.text == f"Лот #{product.id} new text"

    async def test_edited_channel_post_creates_new_mention(self, test_product_type, test_product, test_channel):
        """When edited text adds a new product mention, a new publication is created."""
        async with (
            test_product_type() as ptype,
            test_product(ptype, title="P1") as p1,
            test_product(ptype, title="P2") as p2,
            test_channel(chat_id=445) as channel,
        ):
            await ProductChannelPublication.objects.acreate(
                product=p1, channel=channel, message_id=31, text=f"Лот #{p1.id}", is_main=True
            )
            service = ProductChannelPublicationService()
            await service.edited_channel_post(
                channel_id=channel.chat_id,
                message_id=31,
                text=f"Лот #{p1.id} и Лот #{p2.id}",
            )
            count = await ProductChannelPublication.objects.filter(channel=channel, message_id=31).acount()
            assert count == 2
            pub2 = await ProductChannelPublication.objects.aget(channel=channel, message_id=31, product=p2)
            assert pub2.text == f"Лот #{p1.id} и Лот #{p2.id}"

    async def test_edited_channel_post_sets_is_main_on_update(self, test_product_type, test_product, test_channel):
        """When updating a non-main publication that becomes the only one, is_main is set to True."""
        async with (
            test_product_type() as ptype,
            test_product(ptype, title="P1") as product,
            test_channel(chat_id=446) as channel,
        ):
            pub = await ProductChannelPublication.objects.acreate(
                product=product, channel=channel, message_id=32, text=f"Лот #{product.id}", is_main=False
            )
            service = ProductChannelPublicationService()
            await service.edited_channel_post(
                channel_id=channel.chat_id, message_id=32, text=f"Лот #{product.id} updated"
            )
            await pub.arefresh_from_db()
            assert pub.is_main is True

    async def test_edited_channel_post_deletes_mention_and_updates_remaining(
        self, test_product_type, test_product, test_channel
    ):
        """When a product is removed from the message, its publication is deleted;
        remaining pubs for that product get is_main updated."""
        async with (
            test_product_type() as ptype,
            test_product(ptype, title="P1") as p1,
            test_product(ptype, title="P2") as p2,
            test_channel(chat_id=447) as channel,
        ):
            await ProductChannelPublication.objects.acreate(
                product=p1, channel=channel, message_id=33, text=f"Лот #{p1.id}", is_main=True
            )
            await ProductChannelPublication.objects.acreate(
                product=p2, channel=channel, message_id=33, text=f"Лот #{p1.id} Лот #{p2.id}", is_main=False
            )
            pub_p2_other = await ProductChannelPublication.objects.acreate(
                product=p2, channel=channel, message_id=99, text=f"Лот #{p2.id}", is_main=False
            )
            service = ProductChannelPublicationService()
            await service.edited_channel_post(channel_id=channel.chat_id, message_id=33, text=f"Лот #{p1.id}")
            count_msg33 = await ProductChannelPublication.objects.filter(channel=channel, message_id=33).acount()
            assert count_msg33 == 1
            await pub_p2_other.arefresh_from_db()
            assert pub_p2_other.is_main is True

    async def test_edited_channel_post_delete_skips_empty_and_single_main_remaining(
        self, test_product_type, test_product, test_channel
    ):
        """After delete: product with no remaining publications is skipped;
        product with one main remaining is skipped."""
        async with (
            test_product_type() as ptype,
            test_product(ptype, title="P1") as p1,
            test_product(ptype, title="P2") as p2,
            test_product(ptype, title="P3") as p3,
            test_channel(chat_id=448) as channel,
        ):
            await ProductChannelPublication.objects.acreate(
                product=p1, channel=channel, message_id=34, text=f"Лот #{p1.id}", is_main=True
            )
            await ProductChannelPublication.objects.acreate(
                product=p2, channel=channel, message_id=34, text=f"Лот #{p1.id} Лот #{p2.id}", is_main=False
            )
            text_34 = f"Лот #{p1.id} Лот #{p2.id} Лот #{p3.id}"
            await ProductChannelPublication.objects.acreate(
                product=p3, channel=channel, message_id=34, text=text_34, is_main=False
            )
            await ProductChannelPublication.objects.acreate(
                product=p2, channel=channel, message_id=99, text=f"Лот #{p2.id}", is_main=True
            )
            service = ProductChannelPublicationService()
            await service.edited_channel_post(channel_id=channel.chat_id, message_id=34, text=f"Лот #{p1.id}")
            count_msg34 = await ProductChannelPublication.objects.filter(channel=channel, message_id=34).acount()
            assert count_msg34 == 1
            count_p3 = await ProductChannelPublication.objects.filter(product=p3).acount()
            assert count_p3 == 0
