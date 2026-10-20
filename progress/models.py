from django.db import models
from django.conf import settings
from content.models import Lesson

class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress', verbose_name="Користувач")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress', verbose_name="Урок")
    is_completed = models.BooleanField(default=False, verbose_name="Урок пройдено")
    completion_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата проходження")

    class Meta:
        verbose_name = "Прогрес користувача"
        verbose_name_plural = "Прогрес користувачів"
        unique_together = ['user', 'lesson']

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({'Пройдено' if self.is_completed else 'В процесі'})"


class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz', verbose_name="Урок")
    title = models.CharField(max_length=200, verbose_name="Назва тесту")
    description = models.TextField(blank=True, verbose_name="Опис тесту")

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тести"

    def __str__(self):
        return f"Тест: {self.title} (Урок: {self.lesson.title})"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', verbose_name="Тест")
    text = models.TextField(verbose_name="Текст питання")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок питання")

    class Meta:
        verbose_name = "Питання"
        verbose_name_plural = "Питання"
        ordering = ['order']

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Питання")
    text = models.CharField(max_length=255, verbose_name="Текст відповіді")
    is_correct = models.BooleanField(default=False, verbose_name="Це правильна відповідь")

    class Meta:
        verbose_name = "Відповідь"
        verbose_name_plural = "Відповіді"

    def __str__(self):
        return self.text