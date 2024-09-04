from .base import *

import django_heroku
import os

django_heroku.settings(locals())

if os.environ.get("REDIS_URL"):
    CELERY_BROKER_URL = (
        os.environ.get("REDIS_URL") + "?ssl_cert_reqs=CERT_NONE"
    )
    CELERY_RESULT_BACKEND = (
        os.environ.get("REDIS_URL") + "?ssl_cert_reqs=CERT_NONE"
    )
else:
    CELERY_BROKER_URL = ""
    CELERY_RESULT_BACKEND = ""

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

USE_HTTPS_IN_ABSOLUTE_URLS = True

ALLOWED_HOSTS = VIRTUAL_DOMAINS  # noqa: F405

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "rediss://redis:6379"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"ssl_cert_reqs": None},
        },
    }
}
