from __future__ import annotations

from datetime import date

from pydantic import Field, field_validator

from root.base.entity import BaseEntity, IDMixin
from root.core.enums import SocialsChoices


class SocialEntity(BaseEntity):
    social_type: SocialsChoices
    user_id: str | None = Field(default=None)
    username: str | None = Field(default=None)


class ClientEntity(IDMixin, BaseEntity):
    phone: str | None = Field(default=None)
    surname: str
    name: str
    patronymic: str | None = Field(default=None)
    birth_date: date | None = Field(default=None)
    socials: list[SocialEntity] = Field(default_factory=list)

    @field_validator("phone", mode="before")
    @classmethod
    def field_validator_phone(cls, value):
        return str(value) if value else None
