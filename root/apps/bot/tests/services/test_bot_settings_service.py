from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from root.apps.bot import bot_config
from root.apps.bot.services.bot_settings import BotSettingsService

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


class TestBotSettingsService:
    async def test_get_bot_when_repo_returns_none(self):
        svc = BotSettingsService()
        with patch.object(svc.bot_repo, "get_bot", new_callable=AsyncMock, return_value=None):
            dto = await svc.get_bot("any")
            assert dto.name is None
            assert dto.version is None
            assert dto.description is None
            assert dto.welcome_message is None

    async def test_get_version_when_repo_returns_instance(self):
        svc = BotSettingsService()
        mock_bot = type("Bot", (), {"version": "9.9"})()
        with patch.object(svc.bot_repo, "get_bot", new_callable=AsyncMock, return_value=mock_bot):
            assert await svc.get_version("any") == "9.9"

    async def test_get_bot_when_exists(self, test_bot_model):
        async with test_bot_model(
            name="settings_bot",
            version="2.0",
            description="A test bot",
            welcome_message="Hi",
        ):
            svc = BotSettingsService()
            dto = await svc.get_bot("settings_bot")
            assert dto.name == "settings_bot"
            assert dto.version == "2.0"
            assert dto.description == "A test bot"
            assert dto.welcome_message == "Hi"

    async def test_get_bot_when_not_exists(self):
        svc = BotSettingsService()
        dto = await svc.get_bot("missing_bot")
        assert dto.name is None
        assert dto.version is None
        assert dto.description is None
        assert dto.welcome_message is None

    async def test_get_description_when_exists(self, test_bot_model):
        async with test_bot_model(name="desc_bot", description="My description"):
            svc = BotSettingsService()
            assert await svc.get_description("desc_bot") == "My description"

    async def test_get_description_when_not_exists(self):
        svc = BotSettingsService()
        assert await svc.get_description("missing") is None

    async def test_get_version_when_exists(self, test_bot_model):
        async with test_bot_model(name="ver_bot", version="3.0"):
            svc = BotSettingsService()
            assert await svc.get_version("ver_bot") == "3.0"

    async def test_get_version_when_not_exists_returns_default(self):
        svc = BotSettingsService()
        assert await svc.get_version("missing") == bot_config.DEFAULT_VERSION
