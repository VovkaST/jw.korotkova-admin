from __future__ import annotations

from collections.abc import Callable
from functools import wraps

from telebot import types

from root.apps.bot.application.controllers.user_chats import UserChatController


def store_chat(handler: Callable) -> Callable:
    user_chat_controller = UserChatController()

    @wraps(handler)
    async def wrapped(message: types.Message, *args, **kwargs):
        chat = await user_chat_controller.get_chat(username=message.from_user.username, user_id=message.from_user.id)
        if not chat:
            await user_chat_controller.create_user_chat(
                chat_id=message.chat.id, user_id=message.from_user.id, username=message.from_user.username
            )
        return await handler(message, *args, **kwargs)

    return wrapped
