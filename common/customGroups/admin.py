from django.contrib import admin

from .models import CustomGroup, Membership, Invitation


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "group", "role", "created_at"]


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "group",
        "email",
        "role",
        "is_accepted",
        "unique_code",
    ]


class MembershipInlineAdmin(admin.TabularInline):
    model = Membership
    list_display = ["user", "role"]


@admin.register(CustomGroup)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "unique_code",
        "main_service",
    ]
    inlines = (MembershipInlineAdmin,)
