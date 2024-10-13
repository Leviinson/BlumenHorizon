"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-#mvxx*v8tn1h23&6w^i2q%kzz*ki@$rpox$a^%jy1r0bhuufnq"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv("DEBUG")))

ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0", "localhost"]

INTERNAL_IPS = [
    "0.0.0.0",
    "127.0.0.1",
    "localhost",
]


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "accounts.apps.AccountsConfig",
]

THIRDPARTY_APPS = ["tinymce"]

INSTALLED_APPS = DJANGO_APPS + THIRDPARTY_APPS + LOCAL_APPS

ADMINS = [("Vitalii Melnykov", "melnykov.vitalii197@gmail.com")]

# Mailing
EMAIL_HOST = os.getenv("MAIL_SERVER")
EMAIL_HOST_USER = os.getenv("MAIL_USERNAME")
EMAIL_HOST_PASSWORD = os.getenv("MAIL_PASSWORD")
EMAIL_PORT = int(os.getenv("MAIL_PORT"))
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = os.getenv("SERVER_EMAIL")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["accounts/templates/", "core/staticFiles/"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_NAME"),
        "HOST": os.getenv("MYSQL_HOST"),
        "PORT": os.getenv("MYSQL_PORT"),
        "USER": os.getenv("MYSQL_USER"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD"),
    }
}

# Logging
# https://docs.djangoproject.com/en/5.1/ref/logging/

CELERY_LOG_DIR = os.path.join(BASE_DIR, "logs/celery")
DJANGO_LOG_DIR = os.path.join(BASE_DIR, "logs/django")
REDIS_LOG_DIR = os.path.join(BASE_DIR, "logs/redis")
MYSQL_LOG_DIR = os.path.join(BASE_DIR, "logs/mysql")
LOG_DIRS = [DJANGO_LOG_DIR, CELERY_LOG_DIR, REDIS_LOG_DIR, MYSQL_LOG_DIR]

for log_dir in LOG_DIRS:
    os.makedirs(log_dir, exist_ok=True)

LOGGING_HANDLERS = {
    "django_warning": {
        "level": "WARNING",
        "class": "logging.FileHandler",
        "filename": os.path.join(DJANGO_LOG_DIR, "django_warning.log"),
        "formatter": "django",
    },
    "django_error": {
        "level": "ERROR",
        "class": "logging.FileHandler",
        "filename": os.path.join(DJANGO_LOG_DIR, "django_error.log"),
        "formatter": "django",
    },
    "django_info": {
        "level": "INFO",
        "class": "logging.FileHandler",
        "filename": os.path.join(DJANGO_LOG_DIR, "django_info.log"),
        "formatter": "django",
    },
    "celery_tasks_info": {
        "level": "INFO",
        "class": "logging.FileHandler",
        "filename": os.path.join(CELERY_LOG_DIR, "celery_tasks_info.log"),
        "formatter": "verbose",
    },
    "celery_tasks_error": {
        "level": "ERROR",
        "class": "logging.FileHandler",
        "filename": os.path.join(CELERY_LOG_DIR, "celery_tasks_error.log"),
        "formatter": "verbose",
    },
    "celery_info": {
        "level": "INFO",
        "class": "logging.FileHandler",
        "filename": os.path.join(CELERY_LOG_DIR, "celery_info.log"),
        "formatter": "verbose",
    },
    "celery_error": {
        "level": "ERROR",
        "class": "logging.FileHandler",
        "filename": os.path.join(CELERY_LOG_DIR, "celery_error.log"),
        "formatter": "verbose",
    },
    "mysql_error": {
        "level": "ERROR",
        "class": "logging.FileHandler",
        "filename": os.path.join(MYSQL_LOG_DIR, "mysql_error.log"),
        "formatter": "verbose",
    },
    "redis_error": {
        "level": "ERROR",
        "class": "logging.FileHandler",
        "filename": os.path.join(REDIS_LOG_DIR, "redis_error.log"),
        "formatter": "verbose",
    },
    "mail_admins": (
        {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        }
        if not DEBUG
        else None
    ),
}
LOGGING_HANDLERS = {k: v for k, v in LOGGING_HANDLERS.items() if v is not None}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s: %(levelname)s/%(name)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "django": {
            "format": "[%(asctime)s: %(levelname)s/%(name)s] %(message)s %(status_code)s %(request)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": LOGGING_HANDLERS,
    "loggers": {
        "django.request": {
            "handlers": (
                ["django_error", "django_info", "mail_admins"] if not DEBUG else ["django_error", "django_info", ]
            ),
            "level": "ERROR",
            "propagate": False,
        },
        "django.server": {
            "handlers": (
                ["django_error", "django_info", "mail_admins"] if not DEBUG else ["django_error", "django_info",]
            ),
            "lever": "ERROR",
            "propagate": False,
        },
        "celery.task": {
            "handlers": (
                ["celery_info", "mail_admins"] if not DEBUG else ["celery_info"]
            ),
            "level": "INFO",
            "propagate": False,
        },
        "celery.task": {
            "handlers": (
                ["celery_error", "mail_admins"] if not DEBUG else ["celery_error"]
            ),
            "level": "ERROR",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": (
                ["mysql_error", "mail_admins"] if not DEBUG else ["mysql_error"]
            ),
            "level": "ERROR",
            "propagate": False,
        },
        "django_redis": {
            "handlers": (
                ["redis_error", "mail_admins"] if not DEBUG else ["redis_error"]
            ),
            "level": "ERROR",
            "propagate": False,
        },
    },
} if not DEBUG else None

# Cache
# https://docs.djangoproject.com/en/5.1/topics/cache/#redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        },
    }
}

# Celery
# https://docs.celeryq.dev/en/stable/userguide/application.html#config-from-object

CELERY_BROKER_URL = os.getenv("CELERY_BROKER")
CELERY_RESULT_BACKEND = os.getenv("CELERY_BACKEND")


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    "accounts.backends.UserAuthenticationBackend",
]

AUTH_USER_MODEL = "accounts.User"


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [
    "core/staticfiles/",
    "accounts/templates/",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DJANGO DEBUG TOOLBAR

TESTING = "test" in sys.argv

if not TESTING and DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
