import pytest
from telebot.async_telebot import AsyncTeleBot

from root.apps.bot.application.handlers import handler_new_channel_post

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


class TestNewChannelPostHandler:
    async def test_new_post_without_lots(self, create_channel_post):
        test_bot = AsyncTeleBot("")
        test_bot.register_channel_post_handler(handler_new_channel_post)

        msg = create_channel_post("post content")
        await test_bot.process_new_channel_posts([msg])
