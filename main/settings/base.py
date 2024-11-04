import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

DEBUG = os.environ.get("DEBUG", "False") == "True"
LOCAL_DEV = os.environ.get("LOCAL_DEV", "False") == "True"

CAPTCHA_SITE_KEY = os.getenv("CAPTCHA_SITE_KEY", "")
CAPTCHA_PROJECT = os.getenv("CAPTCHA_PROJECT", "")
GOOGLE_APPLICATION_CREDENTIALS = str(
    {
        "type": "service_account",
        "project_id": os.getenv("GOOGLE_APP_PROJECT_ID", ""),
        "private_key_id": os.getenv("GOOGLE_APP_PRIVATE_KEY_ID", ""),
        "private_key": os.getenv("GOOGLE_APP_PRIVATE_KEY", ""),
        "client_email": os.getenv("GOOGLE_APP_CLIENT_EMAIL", ""),
        "client_id": os.getenv("GOOGLE_APP_CLIENT_ID", ""),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.getenv("GOOGLE_APP_CERT_URL", ""),
    }
)

DATA_UPLOAD_MAX_MEMORY_SIZE = None

DJANGO = [
    "daphne",
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",
    "django.forms",
]

LIBRARIES = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "hijack",
    "hijack.contrib.admin",
    "django_celery_beat",
    "corsheaders",
    "redisboard",
    "anymail",
]

COMMON = [
    "common.users.apps.UserConfig",
    "common.customGroups.apps.GroupConfig",
]

APPS = [
    "homepage.apps.HomepageConfig",
    "rateloaf.apps.RateloafConfig",
    "pdf.apps.PdfConfig",
    "XXXXX_basic.apps.XXXXX_basicConfig",
    "XXXXX_signedin.apps.XXXXX_signedinConfig",
    "XXXXX_websockets.apps.XXXXX_websocketsConfig",
]


INSTALLED_APPS = DJANGO + LIBRARIES + COMMON + APPS


STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "main.virtualhostmiddleware.VirtualHostMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "hijack.middleware.HijackUserMiddleware",
    "sesame.middleware.AuthenticationMiddleware",
]

X_FRAME_OPTIONS = "SAMEORIGIN"

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "common/allauth/templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "common.context_processors.global_context",
            ],
        },
    },
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get("REDIS_URL", "redis://redis:6379")],
        },
    },
}

ASGI_APPLICATION = "main.asgi.application"

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DJANGO_DATABASE_NAME", "main"),
        "USER": os.environ.get("DJANGO_DATABASE_USER", "postgres"),
        "PASSWORD": os.environ.get("DJANGO_DATABASE_PASSWORD", "***"),
        "HOST": os.environ.get("DJANGO_DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("DJANGO_DATABASE_HOST", "5432"),
    }
}

AUTH_USER_MODEL = "users.CustomUser"
LOGIN_REDIRECT_URL = "/"

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

ACCOUNT_ADAPTER = "common.customGroups.adapter.CustomAccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = None
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
SOCIALACCOUNT_QUERY_EMAIL = True
# SOCIALACCOUNT_ADAPTER = "common.customGroups.adapter.SocialAccountAdapter"
SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        'EMAIL_AUTHENTICATION': True,
    },
    "microsoft": {
        "VERIFIED_EMAIL": True,
        'EMAIL_AUTHENTICATION': True,
    },
}

ACCOUNT_FORMS = {
    "signup": "common.customGroups.forms.GroupSignupForm",
}

ACCOUNT_EMAIL_VERIFICATION = os.environ.get("EMAIL_VERIFICATION", "mandatory")


AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "sesame.backends.ModelBackend",
)

SESAME_MAX_AGE = 2 * 60 * 60  # 2 hours

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = BASE_DIR / "static_root"
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
ANYMAIL = {
    "SENDGRID_API_KEY": os.environ.get("SENDGRID_API_KEY", ""),
}

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")

SERVER_EMAIL = os.environ.get("ADMIN_EMAIL", "")
DEFAULT_FROM_EMAIL = os.environ.get("EMAIL", "")
ADMINS = [
    ("Admin", os.environ.get("ADMIN_EMAIL", "")),
]

OPEN_AI_KEY = os.getenv("OPEN_AI_KEY", "")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

CORS_ALLOW_ALL_ORIGINS = True

# Django sites, we are completely ignoring this
SITE_ID = 1

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = "America/New_York"

SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET", "")
SLACK_CLIENT_ID = os.getenv("SLACK_CLIENT_ID", "")
SLACK_CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET", "")
SLACK_SCOPES = os.getenv("SLACK_SCOPES", "commands").split(",")
SLACK_VERIFICATION_TOKEN = os.getenv("SLACK_VERIFICATION_TOKEN", "")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
# Slack Channels
SLACK_GENERAL = os.getenv("SLACK_GENERAL", "")
SLACK_EXCEPTIONS = os.getenv("SLACK_EXCEPTIONS", "")

if LOCAL_DEV:
    USE_HTTPS_IN_ABSOLUTE_URLS = False
else:
    USE_HTTPS_IN_ABSOLUTE_URLS = True

SMARKETMAN_LINK = os.getenv("SMARKETMAN_LINK", "False") == "True"

if LOCAL_DEV and not DEBUG:
    ALLOWED_HOSTS = ["*"]

VIRTUAL_APPS = []
VIRTUAL_DOMAINS = []
VIRTUAL_GOOGLE_ANALYTICS = []
VIRTUAL_GOOGLE_ANALYTICS_API_SECRET = []

for i in range(1, int(os.environ.get("NUMBER_OF_DOMAINS", 0)) + 1):
    domain_key = f"VIRTUAL_DOMAINS_{i}"
    app_key = f"VIRTUAL_APPS_{i}"
    google_analytics_key = f"VIRTUAL_GOOGLE_ANALYTICS_{i}"
    google_analytics_api_key = f"VIRTUAL_GOOGLE_ANALYTICS_API_SECRET_{i}"

    domain_value = os.environ.get(
        domain_key, "localhost:8000" if i == 1 else False
    )

    if domain_value:
        VIRTUAL_APPS.append(os.environ.get(app_key, "XXXXX_basic.urls"))
        VIRTUAL_DOMAINS.append(domain_value)
        VIRTUAL_GOOGLE_ANALYTICS.append(
            os.environ.get(google_analytics_key, "")
        )
        VIRTUAL_GOOGLE_ANALYTICS_API_SECRET.append(
            os.environ.get(google_analytics_api_key, "")
        )

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://redis:6379"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

STRIPE_LIVE_PUBLIC_KEY = os.environ.get(
    "STRIPE_LIVE_PUBLIC_KEY", "<your publishable key>"
)
STRIPE_LIVE_SECRET_KEY = os.environ.get(
    "STRIPE_LIVE_SECRET_KEY", "<your secret key>"
)
STRIPE_TEST_PUBLIC_KEY = os.environ.get(
    "STRIPE_TEST_PUBLIC_KEY", "pk_test_<your publishable key>"
)
STRIPE_TEST_SECRET_KEY = os.environ.get(
    "STRIPE_TEST_SECRET_KEY", "sk_test_<your secret key>"
)

if DEBUG:
    STRIPE_LIVE_MODE = False  # Change to True in production
    STRIPE_PUBLIC_KEY = STRIPE_TEST_PUBLIC_KEY
    STRIPE_PRIVATE_KEY = STRIPE_TEST_SECRET_KEY
else:
    STRIPE_LIVE_MODE = True  # Change to True in production
    STRIPE_PUBLIC_KEY = STRIPE_LIVE_PUBLIC_KEY
    STRIPE_PRIVATE_KEY = STRIPE_LIVE_SECRET_KEY

ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY", "")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
    },
}
