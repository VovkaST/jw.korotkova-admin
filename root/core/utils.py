from __future__ import annotations

import os

import django
import transliterate
from django.contrib import admin
from django.utils.text import slugify as django_slugify
from django.utils.translation import gettext as django_gettext
from django.utils.translation import gettext_lazy as django_gettext_lazy


def gettext(message: str) -> str:
    return django_gettext(message)


def gettext_lazy(message: str) -> str:
    return django_gettext_lazy(message)


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
