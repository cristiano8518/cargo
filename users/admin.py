from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'work_place', 'study_place', 'avatar_preview', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name', 'work_place', 'study_place', 'bio')
    ordering = ('username',)
    list_per_page = 25

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Профиль', {'fields': ('phone', 'avatar', 'work_place', 'study_place', 'bio')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Профиль', {'fields': ('phone', 'avatar', 'work_place', 'study_place', 'bio')}),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="32" height="32" style="border-radius:50%%; object-fit:cover;">', obj.avatar.url)
        return "—"

    avatar_preview.short_description = "Фото"
