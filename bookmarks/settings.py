"""
Django settings for bookmarks project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

from decouple import config
from django.conf import settings
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-+h_bd3-xci%s^#nnq^17g9ll7=dj+j_(n@fp7b1#&-nwyna4#k"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# `mysite.com` is configured in the `hosts` file.
ALLOWED_HOSTS = ["mysite.com", "localhost", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    "account.apps.AccountConfig",  # Place before `django.contrib.admin` to override its templates.
    "django.contrib.admin",  # Includes standard authentication templates.
    "django.contrib.auth",  # Used by other `contrib` packages.
    "django.contrib.contenttypes",  # Used by other `contrib` packages, such as `auth` and `admin`.
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "social_django",
    "django_extensions",
    "easy_thumbnails",
    "django_browser_reload",
    "debug_toolbar",
    "images.apps.ImagesConfig",
    "actions.apps.ActionsConfig",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # Must be placed before any other middleware, except for middleware that encodes the response's content, such as `GZipMiddleware`.
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",  # Handles the session across requests.
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Associate users with requests (`request.user`) using sessions.
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",  # Must be placed after any others that encode the response's content, such as Django's `GZipMiddleware`.
]

ROOT_URLCONF = "bookmarks.urls"

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
                "django.contrib.messages.context_processors.messages",  # Adds `messages` variable to request context.
            ],
        },
    },
]

WSGI_APPLICATION = "bookmarks.wsgi.application"


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

# Authentication framework

LOGIN_REDIRECT_URL = "dashboard"  # Default redirect URL after successful login.
LOGIN_URL = "login"
LOGOUT_URL = "logout"

# Social authentication

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config("GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config("GOOGLE_OAUTH2_SECRET")

SOCIAL_AUTH_PIPELINE = [
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    # "account.authentication.create_profile",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
]

# User credentials will be checked using `ModelBackend`, if no user is returned,
#   credentials will be checked using `EmailAuthBackend`.
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "account.authentication.EmailAuthBackend",
    "social_core.backends.google.GoogleOAuth2",
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [BASE_DIR / "dist"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# SMTP configuration

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Canonical URL - `get_absolute_url()`
# https://docs.djangoproject.com/en/5.1/ref/settings/#absolute-url-overrides

ABSOLUTE_URL_OVERRIDES = {
    # "app_label.model_name" - Model name must be all lowercase.
    "auth.user": lambda user: reverse_lazy("user_detail", args=[user.username]),
}

# django-debug-toolbar

INTERNAL_IPS = [
    "127.0.0.1",
]

# Redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
