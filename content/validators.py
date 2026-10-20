from django.core.exceptions import ValidationError


def validate_course_title(value):
    if len(value.strip()) < 5:
        raise ValidationError(
            "Назва курсу повинна містити щонайменше 5 символів."
        )


def validate_lesson_order(value):
    if value < 0:
        raise ValidationError(
            "Порядковий номер уроку не може бути від'ємним."
        )
