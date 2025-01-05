from __future__ import annotations

from typing import TYPE_CHECKING

from root.apps.notifications.application.boundaries.dtos import NotificationsDailyUpdateDTO
from root.apps.notifications.application.boundaries.notifications_daily import INotificationsDailyRepository
from root.apps.notifications.application.domain.entities import NotificationsDailyEntity
from root.apps.notifications.models import NotificationDaily
from root.base.repository import BaseRepository
from root.core.application.domain.entities import UserEntity

if TYPE_CHECKING:
    from root.apps.notifications.application.domain.enums import NotificationDailyType


class NotificationsDailyRepository(BaseRepository, INotificationsDailyRepository):
    model = NotificationDaily
    base_entity_class = NotificationsDailyEntity
    update_dto_class = NotificationsDailyUpdateDTO

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("users").filter(is_active=True)

    async def get_active_notifications(self, notification_type: NotificationDailyType) -> list[base_entity_class]:
        queryset = self.get_queryset().filter(type=notification_type).all()
        entities = []
        async for notification in queryset:
            entity = await self.to_entity(self.base_entity_class, notification)
            entity.users = [await self.to_entity(UserEntity, user) async for user in notification.users.all()]
            entities.append(entity)
        return entities
