from django.contrib import admin

from .models import CatLoaf


@admin.register(CatLoaf)
class CatLoafAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "unique_name",
        "description",
        "is_rated",
        "is_rating",
    ]
