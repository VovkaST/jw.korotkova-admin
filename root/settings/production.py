from .base import *  # noqa F403

USE_YANDEX_METRIKA = env.bool("USE_YANDEX_METRIKA", default=True)  # noqa F405

USE_SITE_SECURED_PROTOCOL = env.bool("USE_SITE_SECURED_PROTOCOL", default=True)  # noqa F405
