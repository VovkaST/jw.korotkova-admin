from .base import *  # noqa F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=True)  # noqa F405

INSTALLED_APPS.extend(["debug_toolbar", "django_extensions"])  # noqa F405

MIDDLEWARE.extend(["debug_toolbar.middleware.DebugToolbarMiddleware"])  # noqa F405

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])  # noqa F405

INTERNAL_IPS = ["127.0.0.1"]
