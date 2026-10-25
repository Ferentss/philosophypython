
from django.views.generic import ListView, DetailView

from .models import Lesson
from .views import visible_courses, can_manage_course


class LessonListView(ListView):
    model = Lesson
    template_name = "content/lesson_list.html"
    context_object_name = "lessons"
    paginate_by = 10

    def get_queryset(self):
        courses = visible_courses(self.request.user)

        return (
            Lesson.objects
            .filter(course__in=courses)
            .select_related("course", "philosopher")
            .order_by("course__title", "order", "pk")
        )


class LessonDetailView(DetailView):
    model = Lesson
    template_name = "content/lesson_detail.html"
    context_object_name = "lesson"
    pk_url_kwarg = "lesson_pk"

    def get_queryset(self):
        courses = visible_courses(self.request.user)

        return (
            Lesson.objects
            .filter(
                course__in=courses,
                course_id=self.kwargs["course_pk"],
            )
            .select_related("course", "philosopher")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lesson = self.object
        course = lesson.course

        lessons = list(
            course.lessons.order_by("order", "pk")
        )

        previous_lesson = None
        next_lesson = None

        for index, item in enumerate(lessons):
            if item.pk == lesson.pk:
                if index > 0:
                    previous_lesson = lessons[index - 1]

                if index + 1 < len(lessons):
                    next_lesson = lessons[index + 1]

                break

        context["course"] = course
        context["previous_lesson"] = previous_lesson
        context["next_lesson"] = next_lesson
        context["can_manage"] = can_manage_course(
            self.request.user,
            course,
        )

        return context
