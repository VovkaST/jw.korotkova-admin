from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from root.apps.bot.exceptions import UnknownButton
from root.apps.bot.services.buttons import ButtonsService

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


class TestButtonsService:
    async def test_get_button_answer_when_repo_returns_button(self):
        svc = ButtonsService()
        mock_btn = type("Buttons", (), {"simple_response": "mocked response"})()
        with patch.object(svc.buttons_repo, "get_button_by_text", new_callable=AsyncMock, return_value=mock_btn):
            assert await svc.get_button_answer("bot", "Help") == "mocked response"

    async def test_get_buttons_returns_list(self, test_bot_model, test_button):
        async with (
            test_bot_model(name="btn_bot") as bot,
            test_button(bot=bot, text="Btn1", sort_order=1),
            test_button(bot=bot, text="Btn2", sort_order=2),
        ):
            svc = ButtonsService()
            result = await svc.get_buttons("btn_bot")
            assert len(result) == 2
            texts = [b.text for b in result]
            assert "Btn1" in texts and "Btn2" in texts

    async def test_get_buttons_unknown_bot_returns_empty(self):
        svc = ButtonsService()
        result = await svc.get_buttons("nonexistent_bot")
        assert result == []

    async def test_get_button_answer_found(self, test_bot_model, test_button):
        async with (
            test_bot_model(name="ans_bot") as bot,
            test_button(bot=bot, text="Help", simple_response="Here is help"),
        ):
            svc = ButtonsService()
            assert await svc.get_button_answer("ans_bot", "Help") == "Here is help"

    async def test_get_button_answer_unknown_raises(self, test_bot_model):
        async with test_bot_model(name="ans_bot"):
            svc = ButtonsService()
            with pytest.raises(UnknownButton):
                await svc.get_button_answer("ans_bot", "UnknownButton")
