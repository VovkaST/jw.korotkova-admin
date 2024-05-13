import info
from telebot import types
from telebot.async_telebot import AsyncTeleBot

from root.apps.bot.application.domain.const import Commands


async def set_commands(bot: AsyncTeleBot):
    commands = []
    for item in Commands:
        command = types.BotCommand(command=item.name.lower(), description=item.value)
        commands.append(command)
    await bot.set_my_commands(commands)


async def init_bot(bot: AsyncTeleBot):
    await set_commands(bot)
    await bot.set_my_description(info.description)
