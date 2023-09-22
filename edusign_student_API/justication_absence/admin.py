from django.contrib import admin
from .models import Justification

class JustificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'absence_reason', 'date_debut', 'date_fin', 'is_validate')

    list_filter = ('absence_reason', 'is_validate', 'date_debut', 'date_fin')

    search_fields = ('student__email', 'absence_reason', 'date_debut', 'date_fin')

    ordering = ('date_debut',)

    list_per_page = 25

    fieldsets = (
        (None, {
            'fields': ('student', 'absence_reason', 'date_debut', 'date_fin', 'proof_document', 'is_validate')
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

admin.site.register(Justification, JustificationAdmin)

