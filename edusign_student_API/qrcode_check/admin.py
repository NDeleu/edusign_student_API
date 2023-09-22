from django.contrib import admin
from .models import QRCodeGenerator

class QRCodeGeneratorAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'secret_key', 'expiration_time')
    list_filter = ('lesson', 'expiration_time')
    search_fields = ('lesson__name', 'secret_key')
    ordering = ('lesson', 'expiration_time')
    list_per_page = 25
    readonly_fields = ('qr_code',)

    fieldsets = (
        (None, {
            'fields': ('lesson', 'secret_key', 'qr_code', 'expiration_time')
        }),
    )

admin.site.register(QRCodeGenerator, QRCodeGeneratorAdmin)
