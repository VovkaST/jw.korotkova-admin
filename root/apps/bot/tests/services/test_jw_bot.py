from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from root.apps.bot.services.jw_bot import JWBot

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


class TestJWBot:
    async def test_get_name_returns_cached(self):
        jw = JWBot()
        jw._name = "cached_bot"
        assert await jw.get_name() == "cached_bot"

    async def test_get_bot_info_uses_settings_service(self, test_bot_model):
        async with test_bot_model(name="info_bot", version="1.0", description="Desc"):
            jw = JWBot()
            jw._name = "info_bot"
            dto = await jw.get_bot_info()
            assert dto.name == "info_bot"
            assert dto.version == "1.0"
            assert dto.description == "Desc"

    async def test_get_buttons_returns_markup(self, test_bot_model, test_button):
        async with test_bot_model(name="btn_bot") as bot, test_button(bot=bot, text="A"):
            jw = JWBot()
            jw._name = "btn_bot"
            markup = await jw.get_buttons()
            assert markup is not None
            # ReplyKeyboardMarkup has key property for keyboard
            assert hasattr(markup, "keyboard")

    async def test_get_button_answer_returns_response(self, test_bot_model, test_button):
        async with (
            test_bot_model(name="ans_bot") as bot,
            test_button(bot=bot, text="Help", simple_response="Help text"),
        ):
            jw = JWBot()
            jw._name = "ans_bot"
            assert await jw.get_button_answer("Help") == "Help text"

    async def test_get_version_uses_settings_service(self, test_bot_model):
        async with test_bot_model(name="ver_bot", version="2.0"):
            jw = JWBot()
            jw._name = "ver_bot"
            assert await jw.get_version() == "2.0"

    async def test_get_name_calls_bot_when_not_cached(self):
        jw = JWBot()
        jw._name = None
        with patch.object(jw.bot, "get_my_name", new_callable=AsyncMock) as get_my_name:
            from telebot.types import BotName

            get_my_name.return_value = BotName(name="telegram_bot")
            assert await jw.get_name() == "telegram_bot"
            get_my_name.assert_called_once()

    async def test_set_commands_sets_commands_on_bot(self):
        jw = JWBot()
        with patch.object(jw.bot, "set_my_commands", new_callable=AsyncMock) as set_cmd:
            await jw.set_commands()
            set_cmd.assert_called_once()

    async def test_set_description_when_description_exists(self, test_bot_model):
        async with test_bot_model(name="desc_bot", description="Bot description"):
            jw = JWBot()
            jw._name = "desc_bot"
            with patch.object(jw.bot, "set_my_description", new_callable=AsyncMock) as set_desc:
                await jw.set_description()
                set_desc.assert_called_once_with("Bot description")

    async def test_set_description_skips_when_no_description(self):
        jw = JWBot()
        jw._name = "missing_bot"
        with patch.object(jw.bot, "set_my_description", new_callable=AsyncMock) as set_desc:
            await jw.set_description()
            set_desc.assert_not_called()

    async def test_new_channel_post_delegates_to_service(self):
        jw = JWBot()
        with patch.object(
            jw.product_channel_publication_service,
            "new_channel_post",
            new_callable=AsyncMock,
        ) as new_post:
            await jw.new_channel_post(channel_id=-100, message_id=1, text="Hi")
            new_post.assert_called_once_with(-100, 1, "Hi")

    async def test_edited_channel_post_delegates_to_service(self):
        jw = JWBot()
        with patch.object(
            jw.product_channel_publication_service,
            "edited_channel_post",
            new_callable=AsyncMock,
        ) as edited_post:
            await jw.edited_channel_post(channel_id=-100, message_id=1, text="Edited")
            edited_post.assert_called_once_with(-100, 1, "Edited")

    async def test_context_manager_enter_exit(self):
        jw = JWBot()
        async with jw as entered:
            assert entered is jw

    async def test_start_sets_commands_description_and_polls(self):
        jw = JWBot()
        with (
            patch.object(jw, "set_commands", new_callable=AsyncMock) as set_commands,
            patch.object(jw, "set_description", new_callable=AsyncMock) as set_desc,
            patch.object(jw.bot, "polling", new_callable=AsyncMock) as polling,
        ):
            await jw.start()
            set_commands.assert_called_once()
            set_desc.assert_called_once()
            polling.assert_called_once_with(non_stop=True)
