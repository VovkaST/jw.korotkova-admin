from __future__ import annotations

from root.apps.notifications.application.domain.enums import NotificationType
from root.apps.notifications.infrastructure.repositories.notifications_daily import NotificationsDailyRepository


class NotificationsDailyInteractor:
    notifications_daily_repo = NotificationsDailyRepository()

    async def send_daily_notifications(self):
        notifications_daily = await self.notifications_daily_repo.get_active_notifications(NotificationType.BIRTHDAY)
        by_email, by_telegram = [], []
        for notification in notifications_daily:
            for user in notification.users:
                if notification.by_email and user.email:
                    by_email.append(user)
                if notification.by_telegram and user.telegram_id:
                    by_telegram.append(user)
        # todo: отправить уведомления по почте и телеграм
