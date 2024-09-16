from __future__ import annotations

from pydantic import Field

from root.apps.notifications.application.domain.enums import NotificationDailyType
from root.base.entity import BaseEntity, IDMixin
from root.core.application.domain.entities import UserEntity


class NotificationsDailyEntity(IDMixin, BaseEntity):
    mailing_name: str
    type: NotificationDailyType
    by_email: bool
    by_telegram: bool
    is_active: bool
    users: list[UserEntity] = Field(default_factory=list)
