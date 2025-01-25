import copy
from datetime import datetime

import pytest
from telebot import types


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
