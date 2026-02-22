from __future__ import annotations

import pytest

from root.apps.bot.services.channel import ChannelService

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


class TestChannelService:
    async def test_get_channel_by_pk(self, test_channel):
        async with test_channel(chat_id=-999, title="By Pk") as ch:
            svc = ChannelService()
            got = await svc.get_channel(pk=ch.pk)
            assert got is not None
            assert got.pk == ch.pk
            assert got.title == "By Pk"

    async def test_get_channel_by_channel_id(self, test_channel):
        async with test_channel(chat_id=-888, title="By Chat Id") as ch:
            svc = ChannelService()
            got = await svc.get_channel(channel_id=ch.chat_id)
            assert got is not None
            assert got.chat_id == -888
            assert got.title == "By Chat Id"

    async def test_get_channel_not_found_returns_none(self):
        svc = ChannelService()
        assert await svc.get_channel(pk=999999) is None
        assert await svc.get_channel(channel_id=999999) is None

    async def test_create_channel(self):
        svc = ChannelService()
        await svc.create_channel(channel_id=-777, title="Created", link="https://t.me/created")
        got = await svc.get_channel(channel_id=-777)
        assert got is not None
        assert got.title == "Created"
        assert got.link == "https://t.me/created"

    async def test_create_channel_without_link(self):
        svc = ChannelService()
        await svc.create_channel(channel_id=-666, title="No link")
        got = await svc.get_channel(channel_id=-666)
        assert got is not None
        assert got.link in (None, "")
