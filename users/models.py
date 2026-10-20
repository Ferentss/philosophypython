
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_teacher = models.BooleanField(
        default=False,
        verbose_name="Є викладачем"
    )

    is_student = models.BooleanField(
        default=True,
        verbose_name="Є студентом"
    )

    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Про себе"
    )

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self):
        return self.username


class StudentProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="student_profile",
        verbose_name="Користувач"
    )

    enrollment_year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Рік початку навчання"
    )

    interests = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Філософські інтереси"
    )

    class Meta:
        verbose_name = "Профіль студента"
        verbose_name_plural = "Профілі студентів"

    def __str__(self):
        return f"Профіль: {self.user.username}"
