
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
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введіть назву курсу",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Опишіть курс",
                }
            ),
            "status": forms.Select(
                attrs={"class": "form-select"}
            ),
            "is_featured": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()

        if Course.objects.filter(
            title__iexact=title
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Курс із такою назвою вже існує."
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
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                }
            ),
            "philosopher": forms.Select(
                attrs={"class": "form-select"}
            ),
            "order": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
        }


class CourseSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        max_length=100,
        label="Пошук курсів",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Пошук за назвою...",
            }
        )
    )

    published_only = forms.BooleanField(
        required=False,
        label="Тільки опубліковані",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"}
        )
    )
