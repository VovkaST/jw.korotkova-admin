from .base import *  # noqa F403

TEMPLATES[0]["OPTIONS"]["loaders"] = (  # noqa F405
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

CSRF_TRUSTED_ORIGINS = [HOST_NAME]  # noqa F405
