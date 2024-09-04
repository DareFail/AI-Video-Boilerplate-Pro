from django.apps import AppConfig


class UserConfig(AppConfig):
    name = "common.users"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from . import signals  # noqa F401
