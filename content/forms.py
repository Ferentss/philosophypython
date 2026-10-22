
from django import forms
from .models import Course, Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course

        fields = [
            "title",
            "description",
            "status",
            "is_featured",
        ]

        labels = {
            "title": "Назва курсу",
            "description": "Опис курсу",
            "status": "Статус",
            "is_featured": "Рекомендований курс",
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Наприклад: Антична філософія",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 7,
                "placeholder": "Введіть опис курсу",
            }),
            "status": forms.Select(attrs={
                "class": "form-select",
            }),
            "is_featured": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson

        fields = [
            "title",
            "content",
            "philosopher",
            "order",
        ]

        labels = {
            "title": "Назва уроку",
            "content": "Зміст уроку",
            "philosopher": "Пов'язаний філософ",
            "order": "Порядок уроку",
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Наприклад: Філософія Сократа",
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 12,
                "placeholder": "Введіть повний текст уроку",
            }),
            "philosopher": forms.Select(attrs={
                "class": "form-select",
            }),
            "order": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
            }),
        }
