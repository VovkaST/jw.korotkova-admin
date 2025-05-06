from __future__ import annotations

import pydantic_core
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.response import Response

from root.contrib.pydantic.types import ErrorItem
from root.contrib.pydantic.utils import validation_error_format
from root.core.application.domain.exceptions import BaseError, ErrorType


def app_exception_handler(exc: Exception, context):
    """
    Обработчик ошибок для экшенов
    """
    if isinstance(exc, BaseError):
        default_status_code = status.HTTP_400_BAD_REQUEST
        status_map = {
            ErrorType.NOT_FOUND: status.HTTP_404_NOT_FOUND,
            ErrorType.INVALID: status.HTTP_400_BAD_REQUEST,
            # "not_allowed": status.HTTP_403_FORBIDDEN,
            # "too_many_request": status.HTTP_429_TOO_MANY_REQUESTS,
            # "conflict": status.HTTP_409_CONFLICT,
        }
        errors = [ErrorItem(code=exc.code, detail=exc.message)]
        status_code = status_map.get(exc.type, default_status_code)

    elif isinstance(exc, (NotAuthenticated, PermissionDenied)):
        errors = [ErrorItem(code=exc.default_code, detail=exc.detail)]
        status_code = exc.status_code

    elif isinstance(exc, pydantic_core.ValidationError):
        errors = validation_error_format(exc)
        status_code = status.HTTP_400_BAD_REQUEST

    else:
        errors = [ErrorItem(code=ErrorType.NOT_HANDLED, detail=str(exc))]
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return Response({"errors": errors}, status=status_code)
