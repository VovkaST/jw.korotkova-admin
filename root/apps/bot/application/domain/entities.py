"""ChannelEntity kept for cross-app use (e.g. products.application.domain.entities)."""

from __future__ import annotations

from pydantic import Field

from root.base.entity import BaseEntity, IDMixin


class ChannelEntity(IDMixin, BaseEntity):
    chat_id: int
    title: str
    link: str | None = Field(default=None)
