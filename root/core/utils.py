from __future__ import annotations

import os

import django
from django.utils.translation import gettext as django_gettext
from django.utils.translation import gettext_lazy as django_gettext_lazy


def gettext(message: str) -> str:
    return django_gettext(message)


def gettext_lazy(message: str) -> str:
    return django_gettext_lazy(message)


def django_setup():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
    django.setup()
