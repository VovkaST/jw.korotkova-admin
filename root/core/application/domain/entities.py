from __future__ import annotations

from datetime import datetime

from pydantic import Field

from root.base.entity import BaseEntity, IDMixin


class UserEntity(IDMixin, BaseEntity):
    email: str | None
    username: str
    first_name: str
    last_name: str
    patronymic: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    telegram_id: str
    is_active: bool
    is_superuser: bool
    is_staff: bool
    last_login: datetime | None = Field(default=None)
    date_joined: datetime | None = Field(default=None)
