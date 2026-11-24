
import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured


# ============================================================
# BASE CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY is missing. Set it in your .env file."
    )

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in (
    "true", "1", "yes"
)

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "localhost,127.0.0.1"
    ).split(",")
    if host.strip()
]


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    # Third-party applications
    "corsheaders",
    "rest_framework",

    # Local applications
    "api",

    # Django applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # CORS
    "corsheaders.middleware.CorsMiddleware",

    # Django core middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# CORS CONFIGURATION
# ============================================================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

# Do not allow every origin.
CORS_ALLOW_ALL_ORIGINS = False


# ============================================================
# CSRF CONFIGURATION
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "DJANGO_CSRF_TRUSTED_ORIGINS",
        "http://localhost:5173,"
        "http://127.0.0.1:5173,"
        "http://localhost:5174,"
        "http://127.0.0.1:5174"
    ).split(",")
    if origin.strip()
]


# ============================================================
# URL AND SERVER CONFIGURATION
# ============================================================

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ============================================================
# DATABASE - MYSQL
# ============================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv(
            "DB_NAME",
            "career_intelligence_db"
        ),
        "USER": os.getenv(
            "DB_USER",
            "career_app"
        ),
        "PASSWORD": os.getenv(
            "DB_PASSWORD",
            ""
        ),
        "HOST": os.getenv(
            "DB_HOST",
            "127.0.0.1"
        ),
        "PORT": os.getenv(
            "DB_PORT",
            "3307"
        ),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Nairobi"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


# ============================================================
# PRIVATE STUDENT DOCUMENT STORAGE
# ============================================================

# Documents must not be publicly accessible through a media URL.

MEDIA_ROOT = BASE_DIR / "private_media"

FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 MB

DATA_UPLOAD_MAX_MEMORY_SIZE = 6 * 1024 * 1024  # 6 MB


# ============================================================
# EMAIL CONFIGURATION
# ============================================================

if DEBUG:

    # Development: display emails in the terminal
    EMAIL_BACKEND = (
        "django.core.mail.backends.console.EmailBackend"
    )

else:

    # Production: send emails through SMTP
    EMAIL_BACKEND = (
        "django.core.mail.backends.smtp.EmailBackend"
    )

    EMAIL_HOST = os.getenv(
        "DJANGO_EMAIL_HOST",
        "smtp.gmail.com"
    )

    EMAIL_PORT = int(
        os.getenv("DJANGO_EMAIL_PORT", "587")
    )

    EMAIL_HOST_USER = os.getenv(
        "DJANGO_EMAIL_USER",
        ""
    )

    EMAIL_HOST_PASSWORD = os.getenv(
        "DJANGO_EMAIL_PASSWORD",
        ""
    )

    EMAIL_USE_TLS = os.getenv(
        "DJANGO_EMAIL_USE_TLS",
        "True"
    ).lower() in ("true", "1", "yes")

    EMAIL_USE_SSL = False

    EMAIL_TIMEOUT = 10

    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# ============================================================
# DJANGO REST FRAMEWORK
# ============================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],

    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],

    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}


# ============================================================
# JWT AUTHENTICATION
# ============================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),

    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),

    "ROTATE_REFRESH_TOKENS": False,

    "AUTH_HEADER_TYPES": ("Bearer",),

    "AUTH_TOKEN_CLASSES": (
        "rest_framework_simplejwt.tokens.AccessToken",
    ),
}


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# SECURITY SETTINGS
# ============================================================

# Enable HTTPS redirection only when configured for HTTPS.
SECURE_SSL_REDIRECT = os.getenv(
    "DJANGO_SECURE_SSL_REDIRECT",
    "False"
).lower() in ("true", "1", "yes")


# Secure cookies outside development
SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG


# Prevent JavaScript access to session cookies
SESSION_COOKIE_HTTPONLY = True


# HSTS should only be enabled after HTTPS is working properly.
SECURE_HSTS_SECONDS = int(
    os.getenv(
        "DJANGO_SECURE_HSTS_SECONDS",
        "0"
    )
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = False

SECURE_HSTS_PRELOAD = False


# Prevent MIME type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True


# Clickjacking protection
X_FRAME_OPTIONS = "DENY"
