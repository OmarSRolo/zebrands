from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.auth_system.models import Users


class UsersAdmin(UserAdmin):
    def group(self, user):
        if user.is_superuser:
            return "admin"
        groups_all = user.groups.first()
        if groups_all:
            return groups_all.name
        return ""

    group.short_description = "Grupo"

    list_display: list[str] = ['username', 'email', "group", "role"]


admin.site.register(Users, UsersAdmin)
