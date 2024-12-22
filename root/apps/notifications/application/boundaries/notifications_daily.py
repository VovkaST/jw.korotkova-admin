from __future__ import annotations

from abc import ABC, abstractmethod

from root.apps.notifications.application.domain.enums import NotificationDailyType
from root.base.entity import BaseEntityType


class INotificationsDailyRepository(ABC):
    """Repository interface for NotificationsDaily model."""

    @abstractmethod
    async def get_active_notifications(self, notification_type: NotificationDailyType) -> BaseEntityType:
        """Get active notifications by type"""
