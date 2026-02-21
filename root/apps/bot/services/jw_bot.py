from __future__ import annotations

from typing import TYPE_CHECKING

from telebot import logger, types
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateRedisStorage
from telebot.types import BotName

from root.apps.bot import bot_config
from root.apps.bot.enums import Commands
from root.apps.bot.services.bot_settings import BotSettingsService
from root.apps.bot.services.buttons import ButtonsService
from root.apps.products.application.controllers import ProductChannelPublicationController

if TYPE_CHECKING:
    from root.apps.bot.application.boundaries.dtos import BotDTO


class JWBot:
    bot_settings_service = BotSettingsService()
    buttons_service = ButtonsService()
    product_channel_publication_controller = ProductChannelPublicationController()

    def __init__(self) -> None:
        self.config = bot_config
        logger.setLevel(self.config.LOGGING_LEVEL)

        self.bot: AsyncTeleBot = AsyncTeleBot(
            self.config.TOKEN, state_storage=self.get_state_storage()
        )
        self._name: str | None = None

    async def __aenter__(self) -> JWBot:
        return self

    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        pass

    async def get_name(self) -> str:
        if self.bot and not self._name:
            bot_name: BotName = await self.bot.get_my_name()
            self._name = bot_name.name
        return self._name or ""

    async def start(self) -> None:
        await self.set_commands()
        await self.set_description()
        await self.bot.polling(non_stop=True)

    def get_state_storage(self) -> StateRedisStorage:
        return StateRedisStorage(
            redis_url=self.config.REDIS_URL, prefix=self.config.STATE_STORAGE_PREFIX
        )

    async def set_description(self) -> None:
        bot_name = await self.get_name()
        description = await self.bot_settings_service.get_description(bot_name)
        if description:
            await self.bot.set_my_description(description)

    async def set_commands(self) -> None:
        commands = []
        for item in Commands:
            command = types.BotCommand(
                command=item.name.lower(), description=str(item.label)
            )
            commands.append(command)
        await self.bot.set_my_commands(commands)

    async def get_bot_info(self) -> BotDTO:
        bot_name = await self.get_name()
        return await self.bot_settings_service.get_bot(bot_name)

    async def get_buttons(self) -> types.ReplyKeyboardMarkup:
        bot_name = await self.get_name()
        buttons = await self.buttons_service.get_buttons(bot_name)
        inlines = types.ReplyKeyboardMarkup(
            one_time_keyboard=False, resize_keyboard=True
        )
        inlines.add(*[button.text for button in buttons])
        return inlines

    async def get_button_answer(self, button_text: str) -> str:
        bot_name = await self.get_name()
        return await self.buttons_service.get_button_answer(bot_name, button_text)

    async def new_channel_post(
        self, channel_id: int, message_id: int, text: str | None
    ) -> None:
        await self.product_channel_publication_controller.new_channel_post(
            channel_id, message_id, text
        )

    async def edited_channel_post(
        self, channel_id: int, message_id: int, text: str | None
    ) -> None:
        await self.product_channel_publication_controller.edited_channel_post(
            channel_id, message_id, text
        )

    async def get_version(self) -> str:
        bot_name = await self.get_name()
        return await self.bot_settings_service.get_version(bot_name)
