from enum import Enum


class ErrorType(str, Enum):
    INVALID = "invalid"
    NOT_FOUND = "not_found"
    NOT_HANDLED = "not_handled"


class BaseError(Exception):
    code: str
    message: str
    type: str

    def __init__(self, message: str = None, message_code: str = None) -> None:
        self.message = message or self.message
        self.code = message_code or self.code
        super().__init__(self.message)
