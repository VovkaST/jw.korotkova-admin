import inspect
from typing import Any

from django.conf import settings


class AppConfig:
    PREFIX: str = ""

    def __init__(self):
        for attr_name, default_value in inspect.getmembers(self, lambda a: not (inspect.isroutine(a))):
            if attr_name.startswith("_") or attr_name == "PREFIX":
                continue
            setattr(self, attr_name, self._get_from_settings(attr_name, default_value))
        for attr_name, annotation_type in self.__annotations__.items():
            setattr(self, attr_name, self._get_from_settings(attr_name, annotation_type()))

    def _get_from_settings(self, name: str, default: Any = None):
        return getattr(settings, f"{self.PREFIX.upper()}_{name}", default)
