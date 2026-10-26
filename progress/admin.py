
from django.contrib import admin

from .models import Quiz, Question, Answer, Progress


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "lesson",
        "is_completed",
        "completion_date",
    )

    list_filter = (
        "is_completed",
        "completion_date",
    )

    search_fields = (
        "user__username",
        "lesson__title",
    )


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "lesson",
    )

    list_filter = (
        "lesson__course",
    )

    search_fields = (
        "title",
        "description",
        "lesson__title",
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "quiz",
        "order",
    )

    list_filter = (
        "quiz",
    )

    search_fields = (
        "text",
        "quiz__title",
    )

    ordering = (
        "quiz",
        "order",
    )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "question",
        "is_correct",
    )

    list_filter = (
        "is_correct",
    )

    search_fields = (
        "text",
        "question__text",
    )
