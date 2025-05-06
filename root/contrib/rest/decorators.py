from __future__ import annotations

import types
import typing
from collections.abc import Callable, Sequence
from functools import wraps
from typing import Any, get_type_hints

from asgiref.sync import async_to_sync, iscoroutinefunction
from django.http import HttpResponse
from pydantic import BaseModel
from pydantic_core import ValidationError
from rest_framework import status
from rest_framework.decorators import action as drf_action
from rest_framework.request import Request
from rest_framework.response import Response

from root.contrib.pydantic.utils import validation_error_format


def _dump_response_model_function(response):
    is_result_response = False
    content_attr = None
    if isinstance(response, (Response, HttpResponse)):
        is_result_response = True
        content_attr = "data" if isinstance(response, Response) else "content"

    data = getattr(response, content_attr) if is_result_response else response

    if isinstance(data, BaseModel):
        data = data.model_dump()
    elif isinstance(data, Sequence) and not isinstance(data, (str, bytes)):
        data = map(lambda item: item.model_dump() if isinstance(item, BaseModel) else item, data)

    if is_result_response:
        setattr(response, content_attr, data)
    else:
        response = Response(data)

    return response


def dump_response_model_decorator(endpoint):
    @wraps(endpoint)
    def wrapper(*args, **kwargs):
        return _dump_response_model_function(endpoint(*args, **kwargs))

    return wrapper


def is_listed(model: type[BaseModel], field_name: str) -> bool:
    field = model.model_fields.get(field_name)
    if not field:
        return False

    generic_types = [list, set, tuple]

    def _is_iterable_type(annotation):
        if isinstance(annotation, types.UnionType):
            for _type in typing.get_args(annotation):
                if _is_iterable_type(_type):
                    return True
            return False

        return annotation in generic_types or typing.get_origin(annotation) in generic_types

    return _is_iterable_type(field.annotation)


def extract_payload(request: Request, source_key: str, model: type[BaseModel]) -> dict[str, Any]:
    data = {}
    source = getattr(request, source_key)
    for key, value in source.items():
        with_brackets = key.endswith("[]")
        if with_brackets or is_listed(model, key):
            value = [v for v in source.getlist(key) if v != ""]
            if with_brackets:
                key = key[:-2]
        data[key] = value
    return data


def action(
    methods: list[str] | None = None,
    detail: bool | None = False,
    url_path: str | None = None,
    url_name: str | None = None,
    request_model: type[BaseModel] = None,
    response_schema: type | None = None,
    status_map: dict[str, int] | None = None,
    bad_status_code: int | None = status.HTTP_400_BAD_REQUEST,
    base_action_wrapper: Callable | None = drf_action,
    validate_error_response: Callable[[Request, ValidationError], Response] | None = None,
    auto_validate: bool | None = True,
    dump_response_model: bool | None = True,
    **kwargs,
):
    """
    Отмечает метод ViewSet как маршрутизируемое действие (action).
    Функции, декорируемые @action, будут наделены свойством `mapping`, `MethodMapper`,
    которое можно использовать для добавления дополнительных поведений на основе методов
    к маршрутизируемому действию.
    По сути, декоратор расширяет функционал стандартного декоратора`rest_framework.decorators.action`
    (он используется по умолчанию и может быть переопределен).

    Если в аргументах функции указан аргумент, типизированный аналогичной моделью `request_model`,
    то в этот аргумент будет помещен экземпляр провалидированной модели тела запроса.

    :param methods: Список имен HTTP-методов, на которые реагирует это действие.
                    По умолчанию только GET.
    :param detail: Определяет, применимо ли это действие к запросам экземпляров или коллекций.
    :param url_path: Определить сегмент URL для этого действия. По умолчанию используется имя декорированного метода.
    :param url_name: Определить внутренний («обратный») URL-адрес для этого действия.
                     По умолчанию имя метода все знаки подчеркивания заменяются тире.
    :param request_model: Модель для валидации тела запроса и преобразования аргументов.
    :param response_schema: Модель данных ответа. Используется для документации.
    :param status_map: Маппинг кодов http-статусов успешных ответов для различных входящих методов.
    :param bad_status_code: Код ошибочного статуса.
    :param base_action_wrapper: функция обертка для декорирования метода по умолчанию используется
                                (rest_framework.decorators.action).
    :param validate_error_response: функция валидации ответа об ошибке.
    :param auto_validate: Флаг переключения необходимости валидации данных.
    :param dump_response_model: Вызывать model_dump если функция возвращает BaseModel | Sequence[BaseModel].
    :param kwargs: Дополнительные свойства, которые можно установить в представлении.
                   Это можно использовать для переопределения настроек *_classes на уровне набора
                   представлений, что эквивалентно тому, как декораторы `@renderer_classes`
                   и т.д. работают для представлений API на основе функций.
    """

    def decorator(func):
        func = base_action_wrapper(methods=methods, detail=detail, url_path=url_path, url_name=url_name, **kwargs)(func)
        func.request_schema = request_model
        func.response_schema = response_schema
        func.status_map = status_map

        @wraps(func)
        def wrapper(self, request: Request, *args, **kwargs):
            hints = get_type_hints(func)
            if request_model is not None:
                if request.method in ["GET", "DELETE"]:
                    data = extract_payload(request, "query_params", request_model)
                elif "multipart/form-data" in request.content_type:
                    data = extract_payload(request, "data", request_model)
                else:
                    data = request.data.copy()
                if auto_validate:
                    try:
                        request_instance = request_model(**data)
                    except ValidationError as e:
                        if validate_error_response:
                            return validate_error_response(request, e)
                        return Response(status=bad_status_code, data={"errors": validation_error_format(e)})
                    for arg_name, hint in hints.items():
                        if hint is request_model:
                            kwargs[arg_name] = request_instance
            if hints.get("response_schema"):
                kwargs["response_schema"] = response_schema

            if iscoroutinefunction(func):
                result = async_to_sync(func)(self, request, *args, **kwargs)
            else:
                result = func(self, request, *args, **kwargs)

            if result is None:
                result = Response()
            elif dump_response_model:
                result = _dump_response_model_function(result)

            if func.status_map and request.method in func.status_map:
                result.status_code = func.status_map[request.method]
            return result

        return wrapper

    return decorator
