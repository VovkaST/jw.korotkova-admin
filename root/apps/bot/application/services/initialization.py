from __future__ import annotations

import info
from telebot import types
from telebot.async_telebot import AsyncTeleBot

<<<<<<< Current (Your changes)
from root.apps.bot.application.domain.enums import Commands
=======
from root.apps.bot.enums import Commands
>>>>>>> Incoming (Background Agent changes)


async def set_commands(bot: AsyncTeleBot) -> None:
    commands = []
    for item in Commands:
        command = types.BotCommand(
            command=item.name.lower(), description=str(item.label)
        )
        commands.append(command)
    await bot.set_my_commands(commands)


async def init_bot(bot: AsyncTeleBot) -> None:
    await set_commands(bot)
    await bot.set_my_description(info.description)
