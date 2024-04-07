from pydantic import BaseModel, Field


class BotEntity(BaseModel):
    id: int | None
    name: str | None
    version: str | None
    description: str | None
    welcome_message: str | None


class ButtonEntity(BaseModel):
    id: int | None
    bot_id: int | None = Field(default=None)
    text: str | None
    simple_response: str | None
    sort_order: int | None
