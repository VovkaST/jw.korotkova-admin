from .base import *  # noqa F403

DEBUG = env.bool("DJANGO_DEBUG", default=False)  # noqa F405

TEMPLATES[0]["OPTIONS"]["loaders"] = (  # noqa F405
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)
