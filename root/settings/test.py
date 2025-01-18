from .base import *  # noqa F403
from django.utils.translation import gettext_lazy as _

DEBUG = True
REDIS_URL = env.str("REDIS_URL_TEST", default=REDIS_URL)

LANGUAGES = (("ru", _("Russian")),)
