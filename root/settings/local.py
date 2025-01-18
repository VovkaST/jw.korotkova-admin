from .base import *  # noqa F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=True)  # noqa F405

INSTALLED_APPS.append("django_extensions")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])  # noqa F405
