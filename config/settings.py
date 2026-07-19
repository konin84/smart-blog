"""
Minimal settings excerpt — merge into your project's settings.py
(run `django-admin startproject config .` first, then apply these).
"""
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "change-me-in-prod-change-me-in-prod-change-me-in-prod-1234",
)
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",

    "rest_framework",
    "django_filters",
    "corsheaders",

    "blog",
    "users",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",   # must be near the top
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

INSTALLED_APPS += [
    "rest_framework_simplejwt.token_blacklist",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# For production, swap to Postgres, e.g. via dj-database-url + DATABASE_URL env var.

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

USE_CLOUDINARY = os.environ.get("USE_CLOUDINARY", "False") == "True"
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME", ""),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY", ""),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET", ""),
    "SECURE": True,
}
if USE_CLOUDINARY:
    missing = [
        key for key, value in CLOUDINARY_STORAGE.items() if key != "SECURE" and not value
    ]
    if missing:
        raise RuntimeError(
            "Cloudinary is enabled but the following settings are missing: "
            + ", ".join(missing)
        )
    INSTALLED_APPS += ["cloudinary", "cloudinary_storage"]
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
    MEDIA_URL = os.environ.get(
        "CLOUDINARY_MEDIA_URL",
        f"https://res.cloudinary.com/{CLOUDINARY_STORAGE['CLOUD_NAME']}/",
    )
else:
    MEDIA_URL = "media/"
    MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- REST framework ---
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# --- CORS: allow the Next.js frontend origin ---
CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS", "http://localhost:3000"
).split(",")
