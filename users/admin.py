from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, StudentProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "is_teacher",
        "is_student",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_teacher",
        "is_student",
        "is_staff",
        "is_active",
    )

    search_fields = ("username", "email", "first_name", "last_name")

    fieldsets = UserAdmin.fieldsets + (
        (
            "Освітня інформація",
            {
                "fields": (
                    "is_teacher",
                    "is_student",
                    "bio",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Освітня інформація",
            {
                "fields": (
                    "is_teacher",
                    "is_student",
                    "bio",
                )
            },
        ),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "enrollment_year", "interests")
    search_fields = ("user__username", "interests")
    list_filter = ("enrollment_year",)