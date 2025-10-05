import os
from pathlib import Path
from google.cloud import secretmanager
from config.secrets import get_secret

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"
GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")

if os.getenv('GAE_APPLICATION') is not None:
    SECRET_KEY = get_secret("DJANGO_SECRET_KEY", GOOGLE_CLOUD_PROJECT_ID)
    DEBUG = False
    ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

    # Redirects all non-HTTPS requests to HTTPS
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    DATABASES = {
        "default": {
            "ENGINE": get_secret("DB_ENGINE", GOOGLE_CLOUD_PROJECT_ID),
            "HOST": get_secret("DB_HOST", GOOGLE_CLOUD_PROJECT_ID),
            "USER": get_secret("DB_USER", GOOGLE_CLOUD_PROJECT_ID),
            "PASSWORD": get_secret("DB_PASSWORD", GOOGLE_CLOUD_PROJECT_ID),
            "NAME": get_secret("DB_NAME", GOOGLE_CLOUD_PROJECT_ID),
            "PORT": get_secret("DB_PORT", GOOGLE_CLOUD_PROJECT_ID),
        }
    }

else:
    SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
    DEBUG = os.environ.get("DEBUG", "False").lower() in ["true", "1", "yes"]
    ALLOWED_HOSTS = ["*"]

    DATABASES = {
        "default": {
            "ENGINE": os.environ["DB_ENGINE"],
            "HOST": os.environ["DB_HOST"],
            "USER": os.environ["DB_USER"],
            "PASSWORD": os.environ["DB_PASSWORD"],
            "NAME": os.environ["DB_NAME"],
            "PORT": os.environ["DB_PORT"],
        }
    }

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

