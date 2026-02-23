from __future__ import annotations

from django.db.models import QuerySet

from root.apps.notifications.dtos import NotificationsDailyUpdateDTO
from root.apps.notifications.enums import NotificationDailyType
from root.apps.notifications.models import NotificationDaily
from root.base.repository import BaseRepository


class NotificationsDailyRepository(BaseRepository):
    model = NotificationDaily
    update_dto_class = NotificationsDailyUpdateDTO

    def get_queryset(self) -> QuerySet[NotificationDaily]:
        queryset = super().get_queryset()
        return queryset.prefetch_related("users").filter(is_active=True)

    def get_active_notifications(self, notification_type: NotificationDailyType) -> QuerySet[NotificationDaily]:
        return self.get_queryset().prefetch_related("users__socials").filter(type=notification_type)
