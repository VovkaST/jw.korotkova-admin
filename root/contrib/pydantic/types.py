from typing import NotRequired, TypedDict


class ErrorItem(TypedDict):
    code: str
    detail: str
    location: NotRequired[tuple[str | int] | str]
