from django.contrib import admin
from .models import ClassRoom, Lesson, Presence

class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 25

class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_debut', 'date_fin', 'intervening', 'classroom', 'promotion')
    list_filter = ('intervening', 'classroom', 'promotion', 'date_debut', 'date_fin')
    search_fields = ('name', 'intervening__email', 'classroom__name', 'promotion__name')
    ordering = ('date_debut',)
    list_per_page = 25

    fieldsets = (
        (None, {
            'fields': ('name', 'date_debut', 'date_fin', 'description', 'intervening', 'classroom', 'promotion')
        }),
    )

class PresenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'lesson', 'is_present')
    list_filter = ('is_present', 'lesson')
    search_fields = ('student__email', 'lesson__name')
    ordering = ('lesson',)
    list_per_page = 25

    fieldsets = (
        (None, {
            'fields': ('student', 'lesson', 'is_present')
        }),
    )

admin.site.register(ClassRoom, ClassRoomAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Presence, PresenceAdmin)
