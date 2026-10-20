
from django.conf import settings
from django.db import models
from django.urls import reverse

from .validators import validate_course_title, validate_lesson_order


class Era(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Назва епохи"
    )
    description = models.TextField(
        verbose_name="Опис епохи"
    )
    start_year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Рік початку"
    )
    end_year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Рік завершення"
    )

    class Meta:
        verbose_name = "Епоха"
        verbose_name_plural = "Епохи"
        ordering = ["start_year"]

    def __str__(self):
        return self.title


class Philosopher(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Ім'я філософа"
    )
    era = models.ForeignKey(
        Era,
        on_delete=models.CASCADE,
        related_name="philosophers",
        verbose_name="Епоха"
    )
    biography = models.TextField(
        verbose_name="Біографія"
    )
    birth_year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Рік народження"
    )
    death_year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Рік смерті"
    )

    class Meta:
        verbose_name = "Філософ"
        verbose_name_plural = "Філософи"
        ordering = ["birth_year"]

    def __str__(self):
        return self.name


class Course(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Чернетка"
        PUBLISHED = "published", "Опублікований"

    title = models.CharField(
        max_length=200,
        validators=[validate_course_title],
        verbose_name="Назва курсу"
    )
    description = models.TextField(
        verbose_name="Опис курсу"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
        null=True,
        blank=True,
        verbose_name="Викладач"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Статус"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Рекомендований курс"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата оновлення"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курси"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "content:course_detail",
            kwargs={"pk": self.pk}
        )


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Тема уроку"
    )
    content = models.TextField(
        verbose_name="Зміст уроку"
    )
    philosopher = models.ForeignKey(
        Philosopher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons",
        verbose_name="Пов'язаний філософ"
    )
    order = models.PositiveIntegerField(
        default=0,
        validators=[validate_lesson_order],
        verbose_name="Порядок уроку"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["course", "order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Text(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Назва тексту"
    )
    philosopher = models.ForeignKey(
        Philosopher,
        on_delete=models.CASCADE,
        related_name="texts",
        verbose_name="Автор"
    )
    original_content = models.TextField(
        verbose_name="Оригінальний текст"
    )
    translation = models.TextField(
        blank=True,
        verbose_name="Переклад"
    )
    publication_year = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Рік публікації"
    )

    class Meta:
        verbose_name = "Філософський текст"
        verbose_name_plural = "Філософські тексти"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.philosopher.name})"
