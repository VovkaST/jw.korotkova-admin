from __future__ import annotations

from django.utils.translation import gettext
from pydantic import ValidationError

from root.contrib.pydantic.types import ErrorItem


def validation_error_format(
    error: ValidationError, include_url: bool = False, include_context: bool = False, include_input: bool = False
) -> list[ErrorItem]:
    errors = error.errors(include_url=include_url, include_context=include_context, include_input=include_input)
    result = []
    for _error in errors:
        result.append(ErrorItem(code=_error["type"], detail=gettext(_error["msg"]), location=_error["loc"]))
    return result
