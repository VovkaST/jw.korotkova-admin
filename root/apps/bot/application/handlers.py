from telebot import logger, types

from root.apps.bot.application.decorators import store_chat
from root.apps.bot.application.domain.enums import Commands, Messages
from root.apps.bot.application.domain.exceptions import UnknownButton
from root.apps.bot.application.services import bot as bot_instance


@bot_instance.bot.message_handler(commands=["start", Commands.RESTART.name.lower()])
@store_chat
async def handler_start(message: types.Message):
    logger.info("Received %s command [%s@%s]", message.text, message.from_user.id, message.from_user.username)
    inlines = await bot_instance.get_buttons()
    await bot_instance.bot.send_message(message.chat.id, Messages.START.value, reply_markup=inlines)


@bot_instance.bot.message_handler(commands=[Commands.VERSION.name.lower()])
@store_chat
async def handler_version(message: types.Message):
    logger.info("Received %s command [%s@%s]", message.text, message.from_user.id, message.from_user.username)
    version = await bot_instance.get_version()
    inlines = await bot_instance.get_buttons()
    await bot_instance.bot.send_message(message.chat.id, Messages.VERSION.value % version, reply_markup=inlines)


@bot_instance.bot.message_handler(content_types=["text"])
@store_chat
async def handler_messages(message: types.Message):
    logger.info("Received message: %s [%s@%s]", message.text, message.from_user.id, message.from_user.username)
    try:
        answer = await bot_instance.get_button_answer(message.text)
    except UnknownButton:
        logger.info("Unknown message: %s [%s@%s]", message.text, message.from_user.id, message.from_user.username)
        answer = Messages.UNKNOWN.value
    await bot_instance.bot.reply_to(message, answer)
