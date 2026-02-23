from __future__ import annotations

from collections.abc import Callable
from functools import wraps

from telebot import types

from root.apps.bot.services.channel import ChannelService
from root.apps.bot.services.user_chats import UserChatsService


def store_chat(handler: Callable) -> Callable:
    """Decorator for storing user chat. Use it for message handlers."""
    channel_service = ChannelService()
    user_chats_service = UserChatsService()

    @wraps(handler)
    async def wrapped(message: types.Message, *args: object, **kwargs: object):
        match message.chat.type:
            case "channel":
                channel = await channel_service.get_channel(channel_id=message.chat.id)
                if not channel:
                    await channel_service.create_channel(
                        channel_id=message.chat.id,
                        title=message.chat.title,
                        link=message.chat.username,
                    )

            case "private":
                chat = await user_chats_service.get_chat(
                    username=message.from_user.username, user_id=message.from_user.id
                )
                if not chat:
                    await user_chats_service.create_user_chat(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id,
                        username=message.from_user.username,
                    )
        return await handler(message, *args, **kwargs)

    return wrapped
