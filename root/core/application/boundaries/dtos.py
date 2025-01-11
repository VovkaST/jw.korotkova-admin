from pydantic import BaseModel, field_validator


class TelegramChannelConfig(BaseModel):
    link: str
    name: str
    description: str

    @field_validator("description", mode="before")
    @classmethod
    def validate_description(cls, value: str) -> str:
        return str(value) if value else ""


class AppConfig(BaseModel):
    tm_label_text: str
    use_yandex_metrika: bool
    telegram_channel: TelegramChannelConfig
