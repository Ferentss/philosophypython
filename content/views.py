
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import CourseForm, LessonForm
from .models import Course, Era, Lesson, Philosopher


def visible_courses(user):
    queryset = Course.objects.all()

    if user.is_authenticated:
        if user.is_superuser:
            return queryset

        return queryset.filter(
            Q(status=Course.Status.PUBLISHED)
            | Q(owner=user)
        )

    return queryset.filter(status=Course.Status.PUBLISHED)


def home(request):
    eras = Era.objects.all().order_by("start_year")[:5]
    philosophers = Philosopher.objects.select_related("era").all()[:4]

    courses = Course.objects.filter(
        status=Course.Status.PUBLISHED
    ).order_by("-created_at")[:3]

    return render(request, "content/home.html", {
        "eras": eras,
        "philosophers": philosophers,
        "courses": courses,
    })


def philosopher_list(request):
    philosophers = Philosopher.objects.select_related(
        "era"
    ).order_by("name")

    return render(request, "content/philosopher_list.html", {
        "philosophers": philosophers,
    })


def course_list(request):
    courses = Course.objects.filter(
        status=Course.Status.PUBLISHED
    ).order_by("-created_at")

    return render(request, "content/course_list.html", {
        "courses": courses,
    })


def course_detail(request, pk):
    course = get_object_or_404(
        visible_courses(request.user),
        pk=pk,
    )

    lessons = course.lessons.select_related(
        "philosopher"
    ).order_by("order", "pk")

    can_manage = (
        request.user.is_authenticated
        and (
            request.user.is_superuser
            or (
                getattr(request.user, "is_teacher", False)
                and course.owner_id == request.user.pk
            )
        )
    )

    return render(request, "content/course_detail.html", {
        "course": course,
        "lessons": lessons,
        "lesson_count": lessons.count(),
        "can_manage": can_manage,
    })


def lesson_detail(request, course_pk, lesson_pk):
    course = get_object_or_404(
        visible_courses(request.user),
        pk=course_pk,
    )

    lesson = get_object_or_404(
        Lesson.objects.select_related("philosopher"),
        pk=lesson_pk,
        course=course,
    )

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

    can_manage = (
        request.user.is_authenticated
        and (
            request.user.is_superuser
            or (
                getattr(request.user, "is_teacher", False)
                and course.owner_id == request.user.pk
            )
        )
    )

    return render(request, "content/lesson_detail.html", {
        "course": course,
        "lesson": lesson,
        "previous_lesson": previous_lesson,
        "next_lesson": next_lesson,
        "can_manage": can_manage,
    })


class TeacherRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user

        return (
            user.is_authenticated
            and (
                getattr(user, "is_teacher", False)
                or user.is_superuser
            )
        )

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied(
                "Ця сторінка доступна лише викладачам."
            )

        return super().handle_no_permission()


class OwnedCourseMixin(TeacherRequiredMixin):
    def get_queryset(self):
        queryset = Course.objects.all()

        if self.request.user.is_superuser:
            return queryset

        return queryset.filter(owner=self.request.user)


class OwnedLessonMixin(TeacherRequiredMixin):
    def get_queryset(self):
        queryset = Lesson.objects.select_related("course")

        if self.request.user.is_superuser:
            return queryset

        return queryset.filter(
            course__owner=self.request.user
        )


class CourseCreateView(TeacherRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "content/course_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CourseUpdateView(OwnedCourseMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "content/course_form.html"


class CourseDeleteView(OwnedCourseMixin, DeleteView):
    model = Course
    template_name = "content/course_confirm_delete.html"
    success_url = reverse_lazy("content:course_list")


class LessonCreateView(TeacherRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "content/lesson_form.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not (
            getattr(request.user, "is_teacher", False)
            or request.user.is_superuser
        ):
            raise PermissionDenied(
                "Ця сторінка доступна лише викладачам."
            )

        self.course = get_object_or_404(
            Course,
            pk=kwargs["course_pk"],
        )

        if (
            self.course.owner_id != request.user.pk
            and not request.user.is_superuser
        ):
            raise PermissionDenied(
                "Ти не можеш додавати уроки до чужого курсу."
            )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.course = self.course
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "content:course_detail",
            kwargs={"pk": self.course.pk},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = self.course
        return context


class LessonUpdateView(OwnedLessonMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = "content/lesson_form.html"

    def get_success_url(self):
        return reverse(
            "content:course_detail",
            kwargs={"pk": self.object.course_id},
        )


class LessonDeleteView(OwnedLessonMixin, DeleteView):
    model = Lesson
    template_name = "content/lesson_confirm_delete.html"

    def get_success_url(self):
        return reverse(
            "content:course_detail",
            kwargs={"pk": self.object.course_id},
        )