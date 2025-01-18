from __future__ import annotations

from datetime import date, datetime

from pydantic import Field, computed_field, field_validator

from root.base.entity import BaseEntity, IDMixin
from root.core.enums import SocialsChoices


class SiteSettingsEntity(BaseEntity):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    tm_label: str | None = Field(default=None)
    use_yandex_metrika: bool | None = Field(default=False)
    yandex_metrika_code: str | None = Field(default=None)
    telegram_channel: str | None = Field(default=None)
    telegram_channel_description: str | None = Field(default=None)


class SocialEntity(BaseEntity):
    social_type: SocialsChoices
    social_user_id: str | None = Field(default=None)
    social_username: str | None = Field(default=None)


class UserEntity(IDMixin, BaseEntity):
    email: str | None
    username: str
    first_name: str
    last_name: str
    patronymic: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    is_active: bool
    is_superuser: bool
    is_staff: bool
    last_login: datetime | None = Field(default=None)
    date_joined: datetime | None = Field(default=None)
    socials: list[SocialEntity] = Field(default_factory=list)

    @computed_field
    @property
    def telegram(self) -> list[SocialEntity]:
        return [s for s in self.socials if s.social_type == SocialsChoices.TELEGRAM]


class ClientEntity(IDMixin, BaseEntity):
    phone: str | None = Field(default=None)
    last_name: str
    first_name: str
    patronymic: str | None = Field(default=None)
    birth_date: date | None = Field(default=None)
    socials: list[SocialEntity] = Field(default_factory=list)

    @field_validator("phone", mode="before")
    @classmethod
    def field_validator_phone(cls, value):
        return str(value) if value else None
