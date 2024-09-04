from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from common.customGroups.models import Membership

from common.users.models import CustomUser


class MembershipInlineAdmin(admin.TabularInline):
    model = Membership
    list_display = ["group"]


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email"]
    inlines = (MembershipInlineAdmin,)

    fieldsets = UserAdmin.fieldsets
