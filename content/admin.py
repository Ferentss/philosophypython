from django.contrib import admin

from .models import Era, Philosopher, Course, Lesson, Text


@admin.register(Era)
class EraAdmin(admin.ModelAdmin):
    list_display = ("title", "start_year", "end_year")
    search_fields = ("title",)
    ordering = ("start_year",)


@admin.register(Philosopher)
class PhilosopherAdmin(admin.ModelAdmin):
    list_display = ("name", "era", "birth_year", "death_year")
    list_filter = ("era",)
    search_fields = ("name", "biography")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "philosopher", "order")
    list_filter = ("course", "philosopher")
    search_fields = ("title", "content")
    ordering = ("course", "order")


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ("title", "philosopher", "publication_year")
    list_filter = ("philosopher",)
    search_fields = ("title", "original_content", "translation")