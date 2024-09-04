from django.apps import AppConfig


class GroupConfig(AppConfig):
    name = "common.customGroups"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from . import signals  # noqa F401
