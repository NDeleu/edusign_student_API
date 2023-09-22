from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'status', 'promotion', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('status', 'is_active', 'is_staff', 'promotion')
    search_fields = ('id', 'email', 'first_name', 'last_name', 'promotion__name')
    ordering = ('email',)
    list_per_page = 25

    fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'password', 'promotion')
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

    def save_model(self, request, obj, form, change):
        if 'password' in form.cleaned_data:
            obj.set_password(form.cleaned_data['password'])
        elif change:
            existing_user = self.model.objects.get(pk=obj.pk)
            obj.set_password(existing_user.password)
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)
