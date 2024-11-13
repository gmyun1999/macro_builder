"""
Django settings for macro_be project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import sys
from decimal import ROUND_HALF_UP, DefaultContext
from pathlib import Path

import environ
import pymysql

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
env = environ.Env()
environ.Env.read_env(env_file=BASE_DIR / ".env")


ENV = env("ENV", default="localhost")
print(ENV)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

LOG_FILE = "logs/debug.log"
if not os.path.exists("logs"):
    os.mkdir("logs")
open(LOG_FILE, "w").close()

if not os.path.exists("temp"):
    os.mkdir("temp")
    open(LOG_FILE, "w").close()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} || {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            # "formatter": "simple",
        },
        "file": {
            "formatter": "verbose",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/debug.log",
            "backupCount": 1,  # keep at most 10 log files
            "maxBytes": 5 * 1024 * 1024,  # 5*1024*1024 bytes (5MB)
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
        },
    },
}

ALLOWED_HOSTS = ['43.203.255.198']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "user",
    "macro_sheet",
    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = ["*"]

ROOT_URLCONF = "macro_be.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "macro_be.wsgi.application"


# Database

MIGRATION_MODULES = {
    "macro_sheet": "macro_sheet.infra.migrations",
}

pymysql.install_as_MySQLdb()
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
if ENV == "localhost":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "macroAdmin",
            "PASSWORD": env("DB_PASSWORD", default=""),
            "HOST": env("DB_HOST", default=""),
            "PORT": "5432",
            "OPTIONS": {
                "options": "-c search_path=public,content",
            },
            "POOL_OPTIONS": {
                "POOL_SIZE": 30,
                "MAX_OVERFLOW": 10,
                "RECYCLE": 90,
                "PRE_PING": True,
            },
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DefaultContext.rounding = ROUND_HALF_UP

###### ENV
BASE_URL = env("BASE_URL", default="http://127.0.0.1:8000")
SERVICE_URL = env("SERVICE_URL", default="http://localhost:3000")

JWT_SECRET = env("JWT_SECRET", default="JWT_SECRET")
ENC_DEC_KEY = env("ENC_DEC_KEY", default="ENC_DEC_KEY")

HTTPX_TIMEOUT = int(env("HTTPX_TIMEOUT", default="600"))

KAKAO_CLIENT_ID = env("KAKAO_CLIENT_ID", default="KAKAO_CLIENT_ID")
GOOGLE_CLIENT_ID = env("GOOGLE_CLIENT_ID", default="GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = env("GOOGLE_CLIENT_SECRET", default="GOOGLE_CLIENT_SECRET")
PACKAGE_SERVER_URL = env("PACKAGE_SERVER_URL", default="PACKAGE_SERVER_URL")
