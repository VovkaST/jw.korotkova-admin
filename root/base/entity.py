from __future__ import annotations

from typing import Any, TypeVar

from django.db.models.manager import BaseManager
from pydantic import BaseModel, field_validator
from pydantic_core import PydanticUndefined
from pydantic_core.core_schema import ValidationInfo

from root.core.utils import gettext_lazy as _


class BaseEntity(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def get_related_objects_from_manager(cls, value: str, info: ValidationInfo) -> Any:
        if not isinstance(value, BaseManager):
            return value
        field_info = cls.model_fields[info.field_name]
        if field_info.default is not PydanticUndefined:
            return field_info.default
        if field_info.default_factory:
            return field_info.default_factory()
        raise AttributeError(_("Default factory or default value must be specified to related models field"))


BaseEntityType = TypeVar("BaseEntityType", bound=BaseEntity)
