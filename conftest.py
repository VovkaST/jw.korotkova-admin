from collections.abc import Callable
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from root.apps.bot.models import UserChat
from root.core.enums import SocialsChoices
from root.core.models import User, UserSocial
from root.core.utils import removable


async def create_user(
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
    instance = await User.objects.acreate(
        username=username,
        first_name=first_name,
        last_name=last_name,
        patronymic=patronymic,
        birth_date=birth_date,
        phone=phone,
        email=email,
        is_staff=is_staff,
        is_active=is_active,
    )
    return instance


@pytest.fixture(scope="session")
def test_user() -> Callable:
    @removable
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
        return await create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            birth_date=birth_date,
            phone=phone,
            email=email,
            is_staff=is_staff,
            is_active=is_active,
        )

    return _wrapper


@pytest.fixture
def test_staff(test_user) -> Callable:
    @removable
    async def _wrapper(
        username: str,
        first_name: str = "",
        last_name: str = "",
        patronymic: str = None,
        birth_date: datetime = None,
        phone: str = None,
        email: str = "",
        is_active: bool = True,
    ) -> User:
        return await create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            birth_date=birth_date,
            phone=phone,
            email=email,
            is_staff=True,
            is_active=is_active,
        )

    return _wrapper


@pytest.fixture
def test_user_social() -> Callable:
    @removable
    async def _wrapper(
        social_type: SocialsChoices, user: User, social_user_id: str = None, social_username: str = None
    ) -> UserSocial:
        instance, created = await UserSocial.objects.aget_or_create(
            social_type=social_type,
            user=user,
            defaults={"social_user_id": social_user_id, "social_username": social_username},
        )
        return instance

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
    @removable
    async def _wrapper(username: str = None, user_id: str = None, chat_id: str = None) -> UserChat:
        instance = await UserChat.objects.acreate(username=username, user_id=user_id, chat_id=chat_id)
        return instance

    return _wrapper
