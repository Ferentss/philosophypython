
from django import forms
from django.core.exceptions import ValidationError

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
            "status": "Статус курсу",
            "is_featured": "Рекомендований курс",
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Наприклад: Антична філософія",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Коротко опишіть курс",
            }),
            "status": forms.Select(attrs={
                "class": "form-select",
            }),
            "is_featured": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()

        if len(title) < 5:
            raise ValidationError(
                "Назва курсу повинна містити щонайменше 5 символів."
            )

        return title


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
                "placeholder": "Введіть текст уроку",
            }),
            "philosopher": forms.Select(attrs={
                "class": "form-select",
            }),
            "order": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
            }),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()

        if len(title) < 3:
            raise ValidationError(
                "Назва уроку повинна містити щонайменше 3 символи."
            )

        return title


class CourseSearchForm(forms.Form):
    query = forms.CharField(
        label="Пошук курсів",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Знайти курс...",
        }),
    )

    def clean_query(self):
        return self.cleaned_data["query"].strip()
