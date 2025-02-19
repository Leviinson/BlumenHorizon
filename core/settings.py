"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
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
TEST_MODE = os.getenv("ENV") == "test"

ALLOWED_HOSTS = [
    os.getenv("DOMAIN"),
]
INTERNAL_IPS = [
    os.getenv("PUBLIC_IP"),
]

if DEBUG:
    ALLOWED_HOSTS.append("127.0.0.1")
    INTERNAL_IPS.append("127.0.0.1")

# TELEGRAM
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# STRIPE
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")

# DJANGO-TINYMCE
TINYMCE_DEFAULT_CONFIG = {
    "height": 500,
    "width": "100%",
    "plugins": "preview importcss searchreplace autolink autosave save code \
                visualblocks visualchars fullscreen image link media \
                codesample table pagebreak nonbreaking anchor \
                insertdatetime advlist lists wordcount help charmap emoticons quickbars",
    "toolbar": "fullscreen preview | undo redo | bold italic forecolor backcolor | image link | code | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | emoticons ",
    "images_upload_url": "/tinymce-image-upload/",
    "automatic_uploads": True,
    "file_picker_types": "image",
    "custom_undo_redo_levels": 50,
    "quickbars_insert_toolbar": True,
    "file_picker_callback": """function (cb, value, meta) {
        var input = document.createElement("input");
        input.setAttribute("type", "file");
        if (meta.filetype == "image") {
            input.setAttribute("accept", "image/*");
        }
        if (meta.filetype == "media") {
            input.setAttribute("accept", "video/*");
        }

        input.onchange = function () {
            var file = this.files[0];
            var reader = new FileReader();
            reader.onload = function () {
                var id = "blobid" + (new Date()).getTime();
                var blobCache = tinymce.activeEditor.editorUpload.blobCache;
                var base64 = reader.result.split(",")[1];
                var blobInfo = blobCache.create(id, file, base64);
                blobCache.add(blobInfo);
                cb(blobInfo.blobUri(), { title: file.name });
            };
            reader.readAsDataURL(file);
        };
        input.click();
    }""",
    "content_style": "body { font-family:Roboto,Helvetica,Arial,sans-serif; font-size:14px }",
    "valid_children": "+body[title|meta|style|link]",
    "entity_encoding": "raw",
}

DATA_UPLOAD_MAX_MEMORY_SIZE = (
    10485760 // 2
)  # 10MB : 2 = 5MB (for comfort changing in the future)

if DEBUG:
    SECURE_CROSS_ORIGIN_OPENER_POLICY = None
else:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_HOST = os.getenv("DOMAIN")
    SECURE_HSTS_SECONDS = 31536000
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    CORS_ALLOWED_ORIGINS = [
        f'https://{os.getenv("DOMAIN")}',
    ]


if not DEBUG:
    CACHE_MIDDLEWARE_KEY_PREFIX = "athens:"


# Application definition

DJANGO_APPS = [
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
]

LOCAL_APPS = [
    "accounts.apps.AccountsConfig",
    "catalogue.apps.CatalogueConfig",
    "extended_contrib_models.apps.ExtendedContribModelsConfig",
    "cart.apps.CartConfig",
    "mainpage.apps.MainpageConfig",
    "livesearch.apps.LivesearchConfig",
    "wysiwyg.apps.WysiwygConfig",
    "seo.apps.SeoConfig",
    "merchant.apps.MerchantConfig",
]

THIRDPARTY_APPS = [
    "tinymce",
    "rosetta",
    "django_filters",
    "colorfield",
    "rest_framework",
    "cacheops",
]

INSTALLED_APPS = DJANGO_APPS + THIRDPARTY_APPS + LOCAL_APPS

ADMINS = [("Admin", os.getenv("ADMIN_EMAIL"))]

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
    "django.middleware.locale.LocaleMiddleware",
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
        "DIRS": [
            "core/staticfiles/",
        ],
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
        "OPTIONS": {
            "init_command": "SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';",
            "charset": "utf8mb4",
        },
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
    ),
    "telegram_file": {
        "level": "ERROR",
        "class": "logging.FileHandler",
        "filename": os.path.join(BASE_DIR, "logs/telegram/bot.log"),
        "formatter": "verbose",
    },
    "stripe_debug": {
        "level": "DEBUG",
        "class": "logging.FileHandler",
        "filename": os.path.join(BASE_DIR, "logs/stripe/stripe_debug.log"),
        "formatter": "verbose",
    },
    "stripe_info": {
        "level": "INFO",
        "class": "logging.FileHandler",
        "filename": os.path.join(BASE_DIR, "logs/stripe/stripe_info.log"),
        "formatter": "verbose",
    },
    "django_stripe_debug": {
        "level": "DEBUG",
        "class": "logging.FileHandler",
        "filename": os.path.join(BASE_DIR, "logs/stripe/django_stripe_debug.log"),
        "formatter": "verbose",
    },
    "django_stripe_info": {
        "level": "INFO",
        "class": "logging.FileHandler",
        "filename": os.path.join(BASE_DIR, "logs/stripe/django_stripe_info.log"),
        "formatter": "verbose",
    },
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
                ["django_error", "django_info", "mail_admins"]
                if not DEBUG
                else [
                    "django_error",
                    "django_info",
                ]
            ),
            "level": "ERROR",
            "propagate": True,
        },
        "django.server": {
            "handlers": (
                ["django_error", "django_info", "mail_admins"]
                if not DEBUG
                else [
                    "django_error",
                    "django_info",
                ]
            ),
            "level": "ERROR",
            "propagate": True,
        },
        "celery.task": {
            "handlers": (
                ["celery_info", "mail_admins"] if not DEBUG else ["celery_info"]
            ),
            "level": "INFO",
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": (
                ["mysql_error", "mail_admins"] if not DEBUG else ["mysql_error"]
            ),
            "level": "ERROR",
            "propagate": True,
        },
        "django_redis": {
            "handlers": (
                ["redis_error", "mail_admins"] if not DEBUG else ["redis_error"]
            ),
            "level": "ERROR",
            "propagate": True,
        },
        "telegramBot": {
            "handlers": ["telegram_file"],
            "level": "ERROR",
            "propagate": True,
        },
        "stripe": {
            "handlers": ["stripe_debug", "stripe_info"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django_stripe": {
            "handlers": ["django_stripe_debug", "django_stripe_info"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

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
        "KEY_PREFIX": CACHE_MIDDLEWARE_KEY_PREFIX
    }
}

CACHEOPS_REDIS = os.getenv("CACHEOPS_REDIS")
CACHEOPS = {
    "sites.site": {"ops": "all", "timeout": 60 * 15},
    "extended_contrib_models.extendedsite": {"ops": "all", "timeout": 60 * 15},
    "*.*": {"timeout": 60 * 15},
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

PASSWORD_RESET_TIMEOUT = 60 * 15

AUTH_USER_MODEL = "accounts.User"

ROSETTA_LOGIN_URL = "admin:login"
LOGIN_URL = "accounts:signin"
LOGIN_REDIRECT_URL = "accounts:me"
LOGOUT_REDIRECT_URL = "accounts:signin"


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en" if not TEST_MODE else "ru"
LANGUAGES = [
    ("en", "🇺🇸 English"),
    ("de", "🇩🇪 Deutsch"),
    ("ru", "🇷🇺 Русский"),
    ("uk", "🇺🇦 Українська"),
]

TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True
USE_L10N = True
LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [
    "core/staticfiles/",
    "accounts/templates/",
    "catalogue/templates/",
    "cart/templates/",
    "mainpage/templates/",
    MEDIA_ROOT,
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DJANGO DEBUG TOOLBAR
if DEBUG and not TEST_MODE:
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        "debug_toolbar",
    ]
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]


# REGION_SETTINGS ISO 3166-1
PHONENUMBER_DEFAULT_REGION = os.getenv("PHONENUMBER_DEFAULT_REGION")

# SITES
SITE_ID = 1

# CARTON
CART_PRODUCT_LOOKUP = {
    "is_active": True,
    "subcategory__is_active": True,
    "subcategory__category__is_active": True,
}

# REST_FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_THROTTLE_CLASSES": [],
    "DEFAULT_THROTTLE_RATES": {},
}
