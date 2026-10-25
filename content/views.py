
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CourseForm, CourseSearchForm, LessonForm
from .models import Course, Era, Lesson, Philosopher


def visible_courses(user):
    courses = Course.objects.all()

    if user.is_authenticated:
        if user.is_superuser:
            return courses

        return courses.filter(
            Q(status=Course.Status.PUBLISHED)
            | Q(owner=user)
        )

    return courses.filter(status=Course.Status.PUBLISHED)


def can_manage_course(user, course):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    return (
        getattr(user, "is_teacher", False)
        and course.owner_id == user.pk
    )


def home(request):
    eras = Era.objects.all().order_by("start_year")[:5]

    philosophers = Philosopher.objects.select_related(
        "era"
    ).all()[:4]

    courses = Course.objects.filter(
        status=Course.Status.PUBLISHED
    ).order_by("-created_at")[:3]

    return render(request, "content/home.html", {
        "eras": eras,
        "philosophers": philosophers,
        "courses": courses,
    })


class CourseListView(ListView):
    model = Course
    template_name = "content/course_list.html"
    context_object_name = "courses"
    paginate_by = 6

    def get_queryset(self):
        courses = Course.objects.filter(
            status=Course.Status.PUBLISHED
        ).order_by("-created_at")

        self.search_form = CourseSearchForm(self.request.GET)

        if self.search_form.is_valid():
            query = self.search_form.cleaned_data["query"]

            if query:
                courses = courses.filter(
                    Q(title__icontains=query)
                    | Q(description__icontains=query)
                )

        return courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search_form"] = self.search_form

        if self.search_form.is_valid():
            context["search_query"] = (
                self.search_form.cleaned_data["query"]
            )
        else:
            context["search_query"] = ""

        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = "content/course_detail.html"
    context_object_name = "course"

    def get_queryset(self):
        return visible_courses(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lessons = list(
            self.object.lessons.select_related(
                "philosopher"
            ).order_by("order", "pk")
        )

        context["lessons"] = lessons
        context["lesson_count"] = len(lessons)
        context["can_manage"] = can_manage_course(
            self.request.user,
            self.object,
        )

        return context


class PhilosopherListView(ListView):
    model = Philosopher
    template_name = "content/philosopher_list.html"
    context_object_name = "philosophers"

    def get_queryset(self):
        return Philosopher.objects.select_related(
            "era"
        ).order_by("name")


class PhilosopherDetailView(DetailView):
    model = Philosopher
    template_name = "content/philosopher_detail.html"
    context_object_name = "philosopher"

    def get_queryset(self):
        return Philosopher.objects.select_related(
            "era"
        ).prefetch_related("texts")


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

    return render(request, "content/lesson_detail.html", {
        "course": course,
        "lesson": lesson,
        "previous_lesson": previous_lesson,
        "next_lesson": next_lesson,
        "can_manage": can_manage_course(
            request.user,
            course,
        ),
    })


class TeacherRequiredMixin(
    LoginRequiredMixin,
    UserPassesTestMixin,
):
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
        courses = Course.objects.all()

        if self.request.user.is_superuser:
            return courses

        return courses.filter(owner=self.request.user)


class OwnedLessonMixin(TeacherRequiredMixin):
    def get_queryset(self):
        lessons = Lesson.objects.select_related("course")

        if self.request.user.is_superuser:
            return lessons

        return lessons.filter(
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

        if not can_manage_course(request.user, self.course):
            raise PermissionDenied(
                "Ти не можеш змінювати чужий курс."
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


course_list = CourseListView.as_view()
course_detail = CourseDetailView.as_view()
philosopher_list = PhilosopherListView.as_view()
