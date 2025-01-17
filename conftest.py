from collections.abc import Callable
from contextlib import asynccontextmanager
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from root.apps.bot.models import UserChat
from root.core.enums import SocialsChoices
from root.core.models import User, UserSocial


@pytest.fixture(scope="session")
def test_user() -> Callable:
    @asynccontextmanager
    async def _wrapper(
        username: str,
        first_name: str = "",
        last_name: str = "",
        patronymic: str = None,
        birth_date: datetime = None,
        phone: str = None,
        email: str = "",
        is_staff: bool = False,
        is_active: bool = True,
    ) -> User:
        instance, created = await User.objects.aget_or_create(
            username=username,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "patronymic": patronymic,
                "birth_date": birth_date,
                "phone": phone,
                "email": email,
                "is_staff": is_staff,
                "is_active": is_active,
            },
        )
        yield instance
        await instance.adelete()

    return _wrapper


@pytest.fixture
def test_staff(test_user) -> Callable:
    @asynccontextmanager
    async def _wrapper(*args, **kwargs) -> User:
        async with test_user(*args, **kwargs | {"is_staff": True}) as instance:
            yield instance

    return _wrapper


@pytest.fixture
def test_user_social() -> Callable:
    @asynccontextmanager
    async def _wrapper(
        social_type: SocialsChoices, user: User, social_user_id: str = None, social_username: str = None
    ) -> UserSocial:
        instance, created = await UserSocial.objects.aget_or_create(
            social_type=social_type,
            user=user,
            defaults={"social_user_id": social_user_id, "social_username": social_username},
        )
        yield instance
        await instance.adelete()

    return _wrapper


@pytest.fixture
def mock_bot():
    bot = MagicMock()
    bot.send_message = AsyncMock()

    bot_instance = MagicMock()
    bot_instance.bot = bot
    yield bot_instance


@pytest.fixture
def test_user_chat() -> Callable:
    @asynccontextmanager
    async def _wrapper(username: str = None, user_id: str = None, chat_id: str = None) -> UserChat:
        instance = await UserChat.objects.acreate(username=username, user_id=user_id, chat_id=chat_id)
        yield instance
        await instance.adelete()

    return _wrapper
