
from django.contrib import admin

from .models import Era, Philosopher, Course, Lesson, Text


@admin.register(Era)
class EraAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "start_year",
        "end_year",
    )

    list_filter = (
        "start_year",
    )

    search_fields = (
        "title",
        "description",
    )

    ordering = (
        "start_year",
    )


@admin.register(Philosopher)
class PhilosopherAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "era",
        "birth_year",
        "death_year",
    )

    list_filter = (
        "era",
    )

    search_fields = (
        "name",
        "biography",
        "era__title",
    )

    list_select_related = (
        "era",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "status",
        "is_featured",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "is_featured",
        "owner",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "owner__username",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "owner",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "philosopher",
        "order",
    )

    list_filter = (
        "course",
        "philosopher",
    )

    search_fields = (
        "title",
        "content",
        "course__title",
    )

    ordering = (
        "course",
        "order",
    )

    list_select_related = (
        "course",
        "philosopher",
    )


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "philosopher",
        "publication_year",
    )

    list_filter = (
        "philosopher",
    )

    search_fields = (
        "title",
        "original_content",
        "translation",
        "philosopher__name",
    )

    list_select_related = (
        "philosopher",
    )
