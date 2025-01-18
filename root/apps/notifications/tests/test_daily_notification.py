from datetime import date, datetime, timedelta
from unittest.mock import patch

import pytest

from root.apps.notifications.application.interactors.notifications_daily import NotificationsDailyInteractor
from root.core.enums import SocialsChoices

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]

today = datetime.today()
yesterday = datetime.today() - timedelta(days=1)
d1 = date(today.year - 30, today.month, today.day)
d2 = date(today.year - 10, today.month, today.day)
d3 = date(yesterday.year - 20, yesterday.month, yesterday.day)


class TestDailyNotification:
    async def test_no_notifications_planned(self):
        notifications_interactor = NotificationsDailyInteractor()
        result = await notifications_interactor.send_daily_notifications()
        assert result == "No notifications planned"

    async def test_no_birthdays(self, test_notification_daily):
        notifications_interactor = NotificationsDailyInteractor()
        async with test_notification_daily(mailing_name="birthday mailing"):
            result = await notifications_interactor.send_daily_notifications()
        assert result == "No birthday boys found"

    async def test_admin_no_socials(self, test_user, test_staff, test_notification_daily, mock_bot):
        async with test_user("some_user1", first_name="Jack", last_name="London", birth_date=d1), test_staff(
            "some_admin1"
        ) as admin1, test_notification_daily(mailing_name="birthday mailing", users=[admin1], by_telegram=True):
            with patch(
                "root.apps.notifications.application.interactors.notifications_daily.bot_instance", mock_bot
            ) as patched_bot:
                notifications_interactor = NotificationsDailyInteractor()
                result = await notifications_interactor.send_daily_notifications()
        assert result == "Notifications to send: 1, target users: 1, was sent: 0"
        patched_bot.send_message.assert_not_called()

    async def test_admin_has_no_active_bot_chats(
        self, test_user, test_staff, test_notification_daily, test_user_social, mock_bot
    ):
        async with test_user("some_user1", first_name="Jack", last_name="London", birth_date=d1), test_staff(
            "some_admin1"
        ) as admin1, test_user_social(
            SocialsChoices.TELEGRAM, admin1, social_user_id="@admin1_telegram"
        ), test_notification_daily(mailing_name="birthday mailing", users=[admin1], by_telegram=True):
            with patch(
                "root.apps.notifications.application.interactors.notifications_daily.bot_instance", mock_bot
            ) as patched_bot:
                notifications_interactor = NotificationsDailyInteractor()
                result = await notifications_interactor.send_daily_notifications()
        assert result == "Notifications to send: 1, target users: 1, was sent: 0"
        patched_bot.send_message.assert_not_called()

    async def test_success(
        self, test_user, test_staff, test_notification_daily, test_user_social, mock_bot, test_user_chat
    ):
        async with test_user(
            "some_user1", first_name="Jack", last_name="London", birth_date=d1
        ) as user1, test_user_social(
            SocialsChoices.WHATSAPP, user1, social_user_id="@user1_whatsapp"
        ) as user2_telegram, test_user(
            "some_user2", first_name="James", last_name="Bond", birth_date=d2
        ) as user2, test_user("some_user3", first_name="Rowan", last_name="Atkinson", birth_date=d3), test_user_social(
            SocialsChoices.TELEGRAM, user2, social_user_id="@user2_telegram"
        ) as user2_telegram, test_staff("some_admin1") as admin1, test_user_social(
            SocialsChoices.TELEGRAM, admin1, social_user_id="@admin1_telegram"
        ) as admin1_telegram, test_user_chat(
            user_id="123", chat_id="123", username=admin1_telegram.social_user_id
        ) as admin1_chat, test_staff("some_admin2", first_name="mr. Admin") as admin2, test_user_social(
            SocialsChoices.TELEGRAM, admin2, social_user_id="@admin2_telegram"
        ) as admin2_telegram, test_user_chat(
            user_id="456", chat_id="456", username=admin2_telegram.social_user_id
        ) as admin2_chat, test_notification_daily(
            mailing_name="birthday mailing", users=[admin1, admin2], by_telegram=True
        ):
            with patch("root.apps.notifications.application.interactors.notifications_daily.bot_instance", mock_bot):
                notifications_interactor = NotificationsDailyInteractor()
                result = await notifications_interactor.send_daily_notifications()
        assert result == "Notifications to send: 1, target users: 2, was sent: 2"
        assert mock_bot.bot.send_message.await_count == 2
        send1 = mock_bot.bot.send_message.call_args_list[0]
        send2 = mock_bot.bot.send_message.call_args_list[1]

        assert send1.args == (
            "123",
            "some_admin1, не забудь поздравить сегодняшних именинников:\n- London Jack\n- Bond James (@user2_telegram)",
        )
        assert send2.args == (
            "456",
            "mr. Admin, не забудь поздравить сегодняшних именинников:\n- London Jack\n- Bond James (@user2_telegram)",
        )
