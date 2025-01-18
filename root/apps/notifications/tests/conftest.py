from collections.abc import Callable

import pytest

from root.apps.notifications.application.domain.enums import NotificationDailyType
from root.apps.notifications.models import NotificationDaily
from root.core.models import User
from root.core.utils import removable


@pytest.fixture
def test_notification_daily() -> Callable:
    @removable
    async def _wrapper(
        mailing_name: str,
        users: list[User] = None,
        type: NotificationDailyType = NotificationDailyType.BIRTHDAY,
        by_email: bool = False,
        by_telegram: bool = False,
        message_template: str = "",
        is_active: bool = True,
    ) -> NotificationDaily:
        instance = await NotificationDaily.objects.acreate(
            mailing_name=mailing_name,
            type=type,
            by_email=by_email,
            by_telegram=by_telegram,
            message_template=message_template,
            is_active=is_active,
        )
        if users:
            await instance.users.aset(users)
        return instance

    return _wrapper
