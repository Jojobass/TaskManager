from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.db.models import Value
from django.db.models.functions import Concat
from .models import User, Tag, Task
from enum import Enum


class TaskManagerAdminSite(admin.AdminSite):
    pass


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")


@admin.register(User, site=task_manager_admin_site)
class UserAdmin(DefaultUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password", "role")}),
        ("Personal info", {"fields": (("first_name", "last_name"), "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    @admin.display(ordering=Concat("last_name", Value(" "), "first_name"))
    def full_name(self, obj):
        return obj.first_name + " " + obj.last_name

    list_display = ["username", "role", "email", "full_name"]
    list_filter = ["role"]


@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["title"]


@admin.register(Task, site=task_manager_admin_site)
class TaskAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("title",)}),
        ("Description", {"fields": ("description", "priority", "tags")}),
        ("State", {"fields": ("state", "deadline_date", "assignee")}),
        ("Creation data", {"fields": ("author", "created_date", "modified_date")}),
    )
    readonly_fields = ("created_date", "modified_date")
    filter_horizontal = ["tags"]
    list_display = ["title", "state", "priority", "deadline_date", "assignee"]
    list_filter = ["state", "priority", "tags"]
    ordering = ("-priority", "title")
    search_fields = ["title"]
