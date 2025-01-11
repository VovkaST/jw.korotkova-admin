"""
Django settings for chair project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
from logging import getLevelName
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from environ import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
env.read_env(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

HOST_NAME = env.str("HOST_NAME", default=None)
if HOST_NAME:
    if HOST_NAME not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(HOST_NAME)
    if HOST_NAME not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(HOST_NAME)

# Application definition
INSTALLED_APPS = [
    # Django apps
    "root.apps.administration.apps.CoreSiteAdminConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Custom apps
    "root.core",
    "root.apps.clients",
    # "root.apps.orders",
    "root.apps.products",
    "root.apps.bot",
    "root.apps.notifications",
    # Third-party apps
    "phonenumber_field",
    "tinymce",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "root.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["core/templates"],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "root.core.context_processors.app_config",
            ],
            "loaders": (
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ),
        },
    },
]

WSGI_APPLICATION = "root.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {"default": env.db("DATABASE_URL")}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True
USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ("en", _("English")),
    ("ru", _("Russian")),
)

LOCALE_PATHS = (BASE_DIR / "locale",)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "root" / "assets"]

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "core.User"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = ""
EMAIL_PORT = ""
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""

REDIS_URL = env.str("REDIS_URL", default="redis://localhost:6379/0")

PHONENUMBER_DEFAULT_REGION = "RU"

# TM label settings
TM_LABEL_TEXT = env.str("TM_LABEL_TEXT", default="JW.Korotkova")

# Bot settings
BOT_TOKEN = env.str("BOT_TOKEN")
BOT_LOGGING_LEVEL = getLevelName(env.str("BOT_LOGGING_LEVEL", default="INFO"))
BOT_REDIS_URL = REDIS_URL

# Telegram settings and links
TELEGRAM_CHANNEL_LINK_TEMPLATE = "https://t.me/{channel}"
TELEGRAM_CHANNEL_MESSAGE_LINK_TEMPLATE = TELEGRAM_CHANNEL_LINK_TEMPLATE + "/{message_id}"

TELEGRAM_CHANNEL_NAME = env.str("TELEGRAM_CHANNEL_NAME", default="JW_Korotkova")
TELEGRAM_CHANNEL_LINK = TELEGRAM_CHANNEL_LINK_TEMPLATE.format(channel=TELEGRAM_CHANNEL_NAME)
TELEGRAM_CHANNEL_DESCRIPTION = _("Канал живых украшений и трансформаций Натальи Коротковой")

# Celery settings
CELERY_ALWAYS_EAGER = env.bool("CELERY_ALWAYS_EAGER", default=False)
CELERY_BROKER = env.str("CELERY_BROKER", default=REDIS_URL)

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }
