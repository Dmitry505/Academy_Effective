"""
Django settings for locallibrary project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from os import environ as env
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

load_dotenv()

SECRET_KEY: str = env.get("SECRET_KEY", "")

DEBUG: bool = bool(env.get("DEBUG", False))


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "catalog.apps.CatalogConfig",
    "isbn_field",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'csp.middleware.CSPMiddleware',
    'django_ratelimit.middleware.RatelimitMiddleware'
]

ROOT_URLCONF = "locallibrary.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "locallibrary.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth"
                ".password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth"
                ".password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib"
                ".auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib"
                ".auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_ROOT = BASE_DIR / "staticfiles"


STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = "/"

if "DATABASE_URL" in os.environ:
    DATABASES["default"] = dj_database_url.config(
        conn_max_age=500,
        conn_health_checks=True,
    )

STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

ALLOWED_HOSTS = [
    "academyeffective-production.up.railway.app",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = ['https://academyeffective-production.up.railway.app']

# web security
if DEBUG:
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_PRELOAD = False
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    CSP_DEFAULT_SRC = ["'self'"]
    CSP_STYLE_SRC = ["'self'", "https://maxcdn.bootstrapcdn.com"]  # Разрешаем загрузку стилей с Bootstrap
    CSP_SCRIPT_SRC = ["'self'", "https://ajax.googleapis.com", "https://maxcdn.bootstrapcdn.com"]  # Разрешаем загрузку скриптов с jQuery и Bootstrap
   
else:
    # HTTPS
    SECURE_SSL_REDIRECT = True

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    SECURE_HSTS_SECONDS = 31_536_000  # 1 год
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # security headers
    CSP_DEFAULT_SRC = ["'self'"]  # Разрешает загрузку ресурсов только с текущего домена
    CSP_SCRIPT_SRC = ["'self'", "https://cdn.example.com"]  # Разрешает скрипты из указанных источников
    CSP_IMG_SRC = ["'self'", "data:"]  # Разрешает изображения с текущего домена и data: URI
    CSP_FONT_SRC = ["'self'"]  # Разрешает шрифты только с текущего домена
    CSP_CONNECT_SRC = ["'self'"]  # Ограничивает источники для AJAX-запросов
    CSP_FRAME_ANCESTORS = ["'none'"]  # Запрещает встраивание сайта в <iframe> (защита от clickjacking)
    SECURE_CONTENT_TYPE_NOSNIFF = True # Защита от MIME

    # rate limiting
    RATELIMIT_ENABLE = True
    RATELIMIT_GLOBAL = '100/h' # Глобальный лимит на 100 запросов/час на IP
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }