from __future__ import annotations

import os
from collections.abc import Callable
from contextlib import asynccontextmanager
from functools import wraps
from pathlib import Path

import django
import transliterate
from django.contrib import admin
from django.utils.text import slugify as django_slugify
from django.utils.translation import gettext as django_gettext
from django.utils.translation import gettext_lazy as django_gettext_lazy
from django.utils.translation import pgettext_lazy as django_pgettext_lazy


def removable(function) -> Callable:
    """Decorator for async context managers functions that deletes the returned instance after exit."""

    @wraps(function)
    @asynccontextmanager
    async def _wrapper(*args, **kwargs):
        instance = await function(*args, **kwargs)
        yield instance
        await instance.adelete()

    return _wrapper


def gettext(message: str) -> str:
    return django_gettext(message)


def gettext_lazy(message: str) -> str:
    return django_gettext_lazy(message)


def pgettext_lazy(context: str, message: str) -> str:
    return django_pgettext_lazy(context, message)


def get_app_name(file_name: str, parent_level: int = 0) -> str:
    """
    Extract application name of given file name. parent_level indicates what level of pre-parents is app root.
    0 level - is file's parent dir, 1 level is parent's parent (grand parent) and e.t.c.
    """
    full_path = Path(file_name)
    parent = full_path.parents[parent_level]
    return parent.name


def django_setup():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings.local")
    django.setup()


def slugify(text: str) -> str:
    """
    Converts text to slug according to the requirements for that data type.
    In the case when the text is in Cyrillic, it transliterates it.
    """
    return transliterate.slugify(text) or django_slugify(text)


def named_filter(title: str):
    """Returns FieldListFilter with given name."""

    class NamedFieldListFilter(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return NamedFieldListFilter


class Singleton:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance


class DefaultFormatter(dict):
    @staticmethod
    def default(key) -> str:
        return "{" + key + "}"

    def __missing__(self, key):
        return self.default(key)


class ReadOnlyAdminMixin:
    extra = 0  # hide add button on inlines
    can_delete = False  # forbidden deletion on inlines

    def has_add_permission(self, request, obj):
        return False

    def get_readonly_fields(self, request, obj=None):
        if hasattr(self, "fields"):
            return self.fields
        return ()
