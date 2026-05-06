from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'status', 'department', 'year')
    list_filter = ('role', 'status')
    search_fields = ('username', 'email', 'department')
    actions = ['approve_users', 'reject_users']

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('department', 'year', 'role', 'status', 'college_id_image')}),
    )

    @admin.action(description='Approve selected users')
    def approve_users(self, request, queryset):
        queryset.update(status='ACTIVE')

    @admin.action(description='Reject selected users')
    def reject_users(self, request, queryset):
        queryset.update(status='REJECTED')

admin.site.register(CustomUser, CustomUserAdmin)
