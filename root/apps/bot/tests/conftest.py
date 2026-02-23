import copy
from collections.abc import Callable
from datetime import datetime

import pytest
from telebot import types

from root.apps.bot.models import Bot, Buttons, Channel, UserChat
from root.core.utils import removable


def now_as_integer() -> int:
    return int(datetime.now().timestamp())


@pytest.fixture
def create_text_message():
    def _wrapper(text: str) -> types.Message:
        date = now_as_integer()
        params = {"text": text}
        chat = types.Chat(id=11, type=False, title="test_user")
        return types.Message(
            1, from_user=None, date=date, chat=chat, content_type="text", options=params, json_string=""
        )

    return _wrapper


@pytest.fixture
def create_channel_post():
    def _wrapper(text: str) -> types.Message:
        date = now_as_integer()
        sender_chat = types.Chat(id=-11, title="test_channel", type="channel")
        params = {"text": text, "sender_chat": sender_chat}
        chat = copy.deepcopy(sender_chat)
        return types.Message(
            1, from_user=None, date=date, chat=chat, content_type="text", options=params, json_string=""
        )

    return _wrapper


@pytest.fixture
def test_bot_model() -> Callable:
    @removable
    async def _wrapper(
        name: str = "test_bot",
        version: str = "1.0",
        description: str = "Test bot",
        welcome_message: str = "Welcome",
    ) -> Bot:
        return await Bot.objects.acreate(
            name=name,
            version=version,
            description=description,
            welcome_message=welcome_message,
        )

    return _wrapper


@pytest.fixture
def test_button() -> Callable:
    @removable
    async def _wrapper(
        bot: Bot,
        text: str = "Button",
        simple_response: str = "Response",
        sort_order: int = 1,
    ) -> Buttons:
        return await Buttons.objects.acreate(
            bot=bot,
            text=text,
            simple_response=simple_response,
            sort_order=sort_order,
        )

    return _wrapper


@pytest.fixture
def test_channel() -> Callable:
    @removable
    async def _wrapper(
        chat_id: int = -1001234567890,
        title: str = "Test channel",
        link: str | None = None,
    ) -> Channel:
        return await Channel.objects.acreate(chat_id=chat_id, title=title, link=link)

    return _wrapper


@pytest.fixture
def test_user_chat() -> Callable:
    @removable
    async def _wrapper(
        user_id: str = "123",
        chat_id: str = "456",
        username: str | None = "@user",
    ) -> UserChat:
        return await UserChat.objects.acreate(user_id=user_id, chat_id=chat_id, username=username)

    return _wrapper
