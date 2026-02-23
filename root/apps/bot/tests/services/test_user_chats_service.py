from __future__ import annotations

import pytest

from root.apps.bot.enums import ComparisonType
from root.apps.bot.services.user_chats import UserChatsService

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


class TestUserChatsService:
    async def test_get_chat_by_user_id(self, test_user_chat):
        async with test_user_chat(user_id="u1", chat_id="c1", username="@u1") as uc:
            svc = UserChatsService()
            chat_id = await svc.get_chat(user_id="u1")
            assert chat_id == uc.chat_id

    async def test_get_chat_by_username(self, test_user_chat):
        async with test_user_chat(user_id="u2", chat_id="c2", username="@u2"):
            svc = UserChatsService()
            # repo matches by exact username (stored as @u2)
            chat_id = await svc.get_chat(username="@u2")
            assert chat_id == "c2"

    async def test_get_chat_by_username_with_at(self, test_user_chat):
        async with test_user_chat(user_id="u3", chat_id="c3", username="@u3"):
            svc = UserChatsService()
            chat_id = await svc.get_chat(username="@u3")
            assert chat_id == "c3"

    async def test_get_chat_with_or_comparison(self, test_user_chat):
        async with test_user_chat(user_id="u4", chat_id="c4", username="@u4"):
            svc = UserChatsService()
            chat_id = await svc.get_chat(user_id="u4", username="@u4", comparison=ComparisonType.OR)
            assert chat_id == "c4"

    async def test_get_chat_with_and_comparison(self, test_user_chat):
        async with test_user_chat(user_id="u5", chat_id="c5", username="@u5"):
            svc = UserChatsService()
            chat_id = await svc.get_chat(user_id="u5", username="@u5", comparison=ComparisonType.AND)
            assert chat_id == "c5"

    async def test_create_user_chat_then_get_chat(self):
        svc = UserChatsService()
        await svc.create_user_chat(user_id=100, chat_id=200, username="newuser")
        # repo stores username with "@" prefix
        chat_id = await svc.get_chat(username="@newuser")
        assert chat_id == "200"

    async def test_create_user_chat_without_username(self):
        svc = UserChatsService()
        await svc.create_user_chat(user_id="101", chat_id="201")
        chat_id = await svc.get_chat(user_id="101")
        assert chat_id == "201"
