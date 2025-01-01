from pydantic import Field

from root.base.entity import BaseEntity, IDMixin


class ButtonEntity(BaseEntity):
    id: int | None
    bot_id: int | None = Field(default=None)
    text: str | None
    simple_response: str | None
    sort_order: int | None


class BotEntity(BaseEntity):
    id: int | None
    name: str | None
    version: str | None
    description: str | None
    welcome_message: str | None
    buttons: list[ButtonEntity] | None = Field(default_factory=list)


class UserChatEntity(BaseEntity):
    user_id: str
    username: str | None = Field(default=None)
    chat_id: str


class ChannelEntity(IDMixin, BaseEntity):
    chat_id: int
    title: str
