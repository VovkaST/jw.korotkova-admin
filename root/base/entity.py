from __future__ import annotations

from typing import TypeVar

from django.db.models.manager import BaseManager
from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from root.contrib.utils import resource_url
from root.core.enums import ImageSizesChoices
from root.core.utils import gettext as _

_EntityValue = TypeVar("_EntityValue")


class BaseEntity(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def get_related_objects_from_manager(
        cls, value: type[_EntityValue] | None, info: ValidationInfo
    ) -> _EntityValue | list | None:
        if not isinstance(value, BaseManager):
            return value
        if hasattr(value, "all"):
            return value.all()


class IDMixin:
    id: int | None = Field(title=_("Object identity"), default=None)


class ImageMeta(BaseModel):
    size_code: ImageSizesChoices | None = Field(description=_("Images size code"), default=None)
    size: str | None = Field(description=_("Images size (WxH)"), default=None)
    length: int | None = Field(description=_("Images size in bytes"), default=0)


BaseEntityType = TypeVar("BaseEntityType", bound=BaseEntity)
BaseDTOType = TypeVar("BaseDTOType", bound=BaseModel)


def file_url_validator(value) -> str:
    """
    Validates the file url value. If the value is File-field (e.g. not a string and has a 'name' attribute),
    it returns the resource url of the value. Otherwise, it returns the value.
    """
    if not isinstance(value, str) and value.name:
        return resource_url(value.url)
    return value
