from pydantic import BaseModel, Field


class BotDTO(BaseModel):
    name: str | None
    version: str | None
    description: str | None
    welcome_message: str | None


class ButtonDTO(BaseModel):
    bot: BotDTO | None = Field(default=None)
    text: str | None
    simple_response: str | None
    sort_order: int | None
