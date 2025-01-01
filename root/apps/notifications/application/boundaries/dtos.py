from __future__ import annotations

from pydantic import BaseModel, Field, NonNegativeInt

from root.apps.notifications.application.domain.enums import NotificationDailyType


class NotificationsDailyUpdateDTO(BaseModel):
    id: NonNegativeInt
    mailing_name: str | None = Field(default=None)
    type: NotificationDailyType | None = Field(default=None)
    by_email: bool | None = Field(default=None)
    by_telegram: bool | None = Field(default=None)
    message_template: str | None = Field(default=None)
    is_active: bool | None = Field(default=None)
    users: list[NonNegativeInt] = Field(default_factory=list)
