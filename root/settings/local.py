from .base import *  # noqa F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=True)  # noqa F405

INSTALLED_APPS.extend(  # noqa F405
    [
        "debug_toolbar",
        "django_extensions",
        "root.contrib.openapi.redoc_ui",
        "root.contrib.openapi.swagger_ui",
    ]
)

MIDDLEWARE.extend(["debug_toolbar.middleware.DebugToolbarMiddleware"])  # noqa F405

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])  # noqa F405

INTERNAL_IPS = ["127.0.0.1"]
