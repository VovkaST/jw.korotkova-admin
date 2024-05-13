from __future__ import annotations

import logging
from collections.abc import Iterable, Sequence
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum, EnumMeta
from types import NoneType, UnionType
from typing import Any, Optional, TypeVar, Union, get_args, get_type_hints, is_typeddict

from annotated_types import MaxLen
from asgiref.sync import sync_to_async
from django.db.models import ManyToOneRel, Model
from django.db.models.enums import ChoicesType
from django.db.models.fields import NOT_PROVIDED
from django.db.models.fields.related import ForeignKey
from pydantic import BaseModel

from root.contrib.utils import dotval

EntityObjectType = TypeVar("EntityObjectType", bound=BaseModel)
OrmModelObjectType = TypeVar("OrmModelObjectType", bound=Model)
TypedDictObjectType = TypeVar("TypedDictObjectType")


logger = logging.getLogger(__name__)

BASE_TYPES = Union[
    str,
    int,
    float,
    Decimal,
    bool,
    datetime,
    NoneType,
    date,
    time,
    timedelta,
    Enum,
    dict,
]

SEQUENCE_TYPE_NAMES = ["List", "Sequence", "Tuple", "list", "tuple"]


class DictAsObject:
    def __init__(self, data):
        self.__data__ = {}
        for name, value in data.items():
            setattr(self, name, self._wrap(value))
            self.__data__[name] = getattr(self, name)

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)):
            return type(value)([self._wrap(v) for v in value])
        else:
            return DictAsObject(value) if isinstance(value, dict) else value

    def __json__(self):
        return self.__data__


class ObjectMapperService:
    """
    Сервис, который позволяет преобразовывать один тип объекта в другой
    ORM объекты сервис преобразовывать в Entity и наоборот.
    Entity объекты сервис преобразовывать в DTO и наоборот.
    """

    DEFAULT_DEPTH = 0

    @classmethod
    def _is_basic_type(cls, field_type: type) -> bool:
        """
        Метод, для определения, является ли тип базовым(не требуется дополнительных преобразований)
        """
        if field_type == NoneType:
            return True

        if field_type == Any:
            return True

        if cls._is_enum(field_type):
            return True

        if isinstance(field_type, UnionType):
            is_basic = False
            for sub_type in get_args(field_type):
                is_basic = (
                    is_basic
                    or cls._is_enum(sub_type)
                    or (sub_type in get_args(BASE_TYPES) if sub_type != NoneType else False)
                )
            return is_basic
        return field_type in get_args(BASE_TYPES)

    @staticmethod
    def _is_enum(field_type) -> bool:
        """Функция определяет, является ли тип Enum"""
        return type(field_type) in [ChoicesType, EnumMeta]

    @classmethod
    def extract_entity_parent_type(
        cls, field_annotation: type[EntityObjectType] | list | Sequence | tuple | Optional
    ) -> tuple[Any, bool] | tuple[None, bool]:
        """
        Функция получает базовый тип из составного типа, также определяет, является ли составной тип последовательностью.
        @param field_annotation: Составной тип, из которого необходимо получить основной тип,
        можно передать простой тип, тогда функция его и вернет.
        @return: Возвращает кортеж из 2 элементов - тип и признак, является ли поле последовательностью
        """
        field_annotations = get_args(field_annotation)
        # Прямая связь к другой модели
        if not field_annotations:
            return field_annotation, False
        # Optional и может быть None
        elif list(filter(lambda i: i is NoneType, field_annotations)):
            return field_annotations[0], False
        # Последовательность
        elif field_annotation.__name__ in SEQUENCE_TYPE_NAMES:
            return field_annotations[0], True
        return None, False

    @classmethod
    def convert_to_entity(
        cls,
        entity_class: type[EntityObjectType],
        obj_to_convert: OrmModelObjectType | TypedDictObjectType | dict,
        **kwargs,
    ) -> EntityObjectType:
        """
        Метод для конвертации объекта в Entity объект.
        Entity объект должен быть наследован от BaseModel модуля pydantic.
        Поддерживает конвертации связанных объектов.
        @param entity_class: Объект, который будет возвращен из функции.
        @param obj_to_convert: Объект, из которого необходимо брать данные.
        @param kwargs:
            - depth: Опциональный параметр, глубина преобразования вложенных объектов, по умолчанию равняется 1
            - mapping: Опциональный параметр, словарь, который изменяет получение какого то из полей.
            - include_relation: Опциональный параметр, список полей, связи с которыми необходимо создавать.
                Если не указано, то будут создаваться все связи.
            - exclude: Опциональный параметр, список полей, которые необходимо исключить при создании
        @return: entity_class
        """
        depth = kwargs.pop("depth", cls.DEFAULT_DEPTH)
        mapping = kwargs.pop("mapping", {})
        include_relation = kwargs.pop("include_relation", [])
        exclude = kwargs.pop("exclude", [])
        result_dict = {}

        if isinstance(obj_to_convert, dict):
            obj_to_convert = DictAsObject(obj_to_convert)

        for model_name, model_field in entity_class.model_fields.items():
            logger.debug(f"convert_to_entity loop started: {model_name=}, {model_field=}")
            if model_name in exclude:
                continue
            if cls._is_basic_type(model_field.annotation) or isinstance(
                dotval(obj_to_convert, mapping.get(model_name) or model_name), BaseModel
            ):
                result_dict[model_name] = dotval(obj_to_convert, mapping.get(model_name) or model_name)
            else:
                # Получаем связанный с полем тип
                parent_type, many = cls.extract_entity_parent_type(model_field.annotation)

                if not parent_type:
                    raise ValueError(f"Missing annotation for {entity_class=}, {model_name=}")

                # Для Optional полей проваливаемся в рекурсию, только если есть связь,
                # иначе считаем, что это базовый тип TypeError, если была передана последовательность(list например)
                try:
                    if not issubclass(parent_type, BaseModel):
                        result_dict[model_name] = dotval(obj_to_convert, mapping.get(model_name) or model_name)
                        continue
                except TypeError:
                    pass
                # Превысили глубину, значит не заполняем поле
                if depth <= 0 or (include_relation and model_name not in include_relation):
                    continue
                # Если связь единичная, то вызываем рекурсию с depth - 1 для связанного объекта
                if not many:
                    value = dotval(obj_to_convert, mapping.get(model_name) or model_name)
                    if value is not None:
                        result_dict[model_name] = cls.convert_to_entity(
                            parent_type, value, depth=depth - 1, mapping=mapping, exclude=exclude
                        )
                # Иначе ожидаем, что нужна последовательность,
                # запускаем рекурсию для каждого связанного объекта в последовательности с depth - 1
                else:
                    value = dotval(obj_to_convert, mapping.get(model_name) or model_name)
                    # Если значение и так Iterable, то берем его
                    if isinstance(value, Iterable):
                        values = value
                    # Если нет, то проверяем, есть ли у него all метод и вызываем его
                    elif hasattr(value, "all") and callable(value.all):
                        values = value.all()
                    # Кидаем исключение, о том, что связь должна быть Iterable
                    elif value is None:
                        continue
                    else:
                        raise ValueError(f"Annotation is {parent_type}, but value is not iterable")
                    result_dict[model_name] = [
                        cls.convert_to_entity(parent_type, value, depth=depth - 1, mapping=mapping, exclude=exclude)
                        for value in values
                    ]
        return entity_class(**result_dict)

    @classmethod
    def convert_to_orm(
        cls,
        orm_class: type[OrmModelObjectType],
        obj_to_convert: EntityObjectType | TypedDictObjectType | dict,
        **kwargs,
    ) -> OrmModelObjectType:
        """
        Метод для конвертации объекта в Django ORM модель
        @param orm_class: Объект, который будет возвращен из функции.
        @param obj_to_convert: Объект, из которого необходимо брать данные.
        @param kwargs:
            - depth: Опциональный параметр, глубина преобразования вложенных объектов, по умолчанию равняется 1
            - exclude: Опциональный параметр, список полей, которые необходимо исключить при создании
        @return: entity_class
        """
        result_dict = {}
        mapping = kwargs.pop("mapping", {})
        exclude = kwargs.pop("exclude", [])

        if isinstance(obj_to_convert, dict):
            obj_to_convert = DictAsObject(obj_to_convert)

        for orm_field in orm_class._meta.get_fields():
            if orm_field.name in exclude:
                continue
            value = dotval(obj_to_convert, mapping.get(orm_field.name) or orm_field.name)
            if (
                isinstance(orm_field, ManyToOneRel)
                or not value
                and (not orm_field.default or orm_field.default == NOT_PROVIDED)
            ):
                continue
            elif isinstance(orm_field, ForeignKey):
                result_dict[f"{orm_field.name}_id"] = dotval(
                    obj_to_convert, mapping.get(f"{orm_field.name}_id") or f"{orm_field.name}_id"
                )
            else:
                result_dict[orm_field.name] = value
        return orm_class(**result_dict)

    @classmethod
    def _get_dto_type(cls, dto_field: type[Any]) -> type[TypedDictObjectType | Any]:
        """
        Функция получает базовый тип DTO, из составного, если тип является составным,
        иначе возвращает тот же тип, который и был передан.
        @param dto_field: Тип, указанный при объявлении DTO поля.
        @return: Возвращает тип поля.
        """
        args = get_args(dto_field)
        if args:
            return cls._get_dto_type(args[0])
        return dto_field

    @classmethod
    def convert_to_dto(
        cls, dto_class: type[TypedDictObjectType], obj_to_convert: EntityObjectType | dict, **kwargs
    ) -> TypedDictObjectType:
        """
        Метод для конвертации объекта в Django ORM модель
        @param dto_class: Объект, который будет возвращен из функции.
        @param obj_to_convert: Объект, из которого необходимо брать данные.
        @param kwargs:
            - mapping: Опциональный параметр, словарь, который изменяет получение какого то из полей.
            - exclude: Опциональный параметр, список полей, которые необходимо исключить при создании
        @return: entity_class
        """
        result_dict = {}
        mapping = kwargs.pop("mapping", {})
        exclude = kwargs.pop("exclude", [])

        if isinstance(obj_to_convert, dict):
            obj_to_convert = DictAsObject(obj_to_convert)

        for dto_name, dto_value in get_type_hints(dto_class).items():
            if dto_name in exclude:
                continue
            field_type = cls._get_dto_type(dto_value)
            if is_typeddict(field_type) or issubclass(field_type, BaseModel):
                value = dotval(obj_to_convert, mapping.get(dto_name) or dto_name)
                if not value:
                    continue
                if (
                    getattr(dto_value, "__name__", None) in SEQUENCE_TYPE_NAMES
                    or (arg := get_args(dto_value))
                    and arg[0] in SEQUENCE_TYPE_NAMES
                ):
                    value = [
                        cls.convert_to_dto(field_type, val_item, mapping=mapping, exclude=exclude) for val_item in value
                    ]
                else:
                    value = cls.convert_to_dto(field_type, value, mapping=mapping, exclude=exclude)
            else:
                value = dotval(obj_to_convert, mapping.get(dto_name) or dto_name)
            result_dict[dto_name] = value
        return dto_class(**result_dict)


@sync_to_async
def create_dto_object(dto_class, entity_object, mappings=None, exclude=None):
    if mappings is None:
        mappings = {}
    if exclude is None:
        exclude = []
    return ObjectMapperService.convert_to_dto(dto_class, entity_object, mapping=mappings, exclude=exclude)


def create_entity_object(
    entity_class: type[EntityObjectType],
    db_object,
    mappings: dict | None = None,
    exclude=None,
    depth=0,
    include_relation=None,
) -> EntityObjectType:
    """
    :type depth: Актуально когда нужно создать entity со вложенными сущностями (depth=1).
    """
    if mappings is None:
        mappings = {}
    if exclude is None:
        exclude = []
    if include_relation is None:
        include_relation = []

    return ObjectMapperService.convert_to_entity(
        entity_class, db_object, mapping=mappings, exclude=exclude, depth=depth, include_relation=include_relation
    )


def get_max_length_from_entity(entity_class: type[EntityObjectType], field_name: str) -> int | None:
    """Получение свойства максимальной длинны поля"""
    if entity_class and field_name in entity_class.model_fields:
        field = entity_class.model_fields[field_name]
        for metadata_param in field.metadata:
            if isinstance(metadata_param, MaxLen):
                return metadata_param.max_length
