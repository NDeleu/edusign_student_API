from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'status', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('status', 'is_active', 'is_staff')
    search_fields = ('id', 'email', 'first_name', 'last_name')
    ordering = ('email',)
    list_per_page = 25

    fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'password')
        }),
        ('Permissions', {
            'fields': ('status', 'is_active', 'is_staff', 'is_superuser')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
