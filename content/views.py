
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import CourseForm, CourseSearchForm
from .models import Era, Philosopher, Course, Lesson, Text


def home(request):
    eras = Era.objects.all()
    philosophers = Philosopher.objects.select_related("era").all()

    courses = Course.objects.select_related("owner").filter(
        status=Course.Status.PUBLISHED
    )

    context = {
        "eras": eras,
        "philosophers": philosophers,
        "courses": courses,
        "featured_courses": courses.filter(is_featured=True)[:3],
        "latest_courses": courses[:6],
        "texts": Text.objects.select_related("philosopher").all()[:6],
    }

    return render(request, "content/home.html", context)


class CourseListView(ListView):
    model = Course
    template_name = "content/course_list.html"
    context_object_name = "courses"
    paginate_by = 6

    def get_queryset(self):
        queryset = Course.objects.select_related("owner")

        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(status=Course.Status.PUBLISHED)
                | Q(owner=self.request.user)
            )
        else:
            queryset = queryset.filter(
                status=Course.Status.PUBLISHED
            )

        self.search_form = CourseSearchForm(self.request.GET)

        if self.search_form.is_valid():
            query = self.search_form.cleaned_data.get("query")
            published_only = self.search_form.cleaned_data.get(
                "published_only"
            )

            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query)
                    | Q(description__icontains=query)
                )

            if published_only:
                queryset = queryset.filter(
                    status=Course.Status.PUBLISHED
                )

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.search_form
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = "content/course_detail.html"
    context_object_name = "course"

    def get_queryset(self):
        queryset = Course.objects.select_related("owner")

        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(status=Course.Status.PUBLISHED)
                | Q(owner=self.request.user)
            )

        return queryset.filter(
            status=Course.Status.PUBLISHED
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["lessons"] = self.object.lessons.select_related(
            "philosopher"
        ).all()

        context["can_manage"] = (
            self.request.user.is_authenticated
            and self.object.owner_id == self.request.user.pk
            and (
                self.request.user.is_staff
                or getattr(self.request.user, "is_teacher", False)
            )
        )

        return context


class TeacherRequiredMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user

        return (
            user.is_authenticated
            and (
                user.is_staff
                or getattr(user, "is_teacher", False)
            )
        )


class CourseCreateView(
    LoginRequiredMixin,
    TeacherRequiredMixin,
    CreateView
):
    model = Course
    form_class = CourseForm
    template_name = "content/course_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CourseUpdateView(
    LoginRequiredMixin,
    TeacherRequiredMixin,
    UpdateView
):
    model = Course
    form_class = CourseForm
    template_name = "content/course_form.html"

    def get_queryset(self):
        return Course.objects.filter(
            owner=self.request.user
        )


class CourseDeleteView(
    LoginRequiredMixin,
    TeacherRequiredMixin,
    DeleteView
):
    model = Course
    template_name = "content/course_confirm_delete.html"
    success_url = reverse_lazy("content:course_list")

    def get_queryset(self):
        return Course.objects.filter(
            owner=self.request.user
        )


class LessonDetailView(DetailView):
    model = Lesson
    template_name = "content/lesson_detail.html"
    context_object_name = "lesson"

    def get_queryset(self):
        queryset = Lesson.objects.select_related(
            "course",
            "philosopher",
            "course__owner",
        )

        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(course__status=Course.Status.PUBLISHED)
                | Q(course__owner=self.request.user)
            )

        return queryset.filter(
            course__status=Course.Status.PUBLISHED
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["course"] = self.object.course
        context["lessons"] = self.object.course.lessons.all()

        return context


class EraListView(ListView):
    model = Era
    template_name = "content/era_list.html"
    context_object_name = "eras"
    paginate_by = 10


class EraDetailView(DetailView):
    model = Era
    template_name = "content/era_detail.html"
    context_object_name = "era"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["philosophers"] = self.object.philosophers.all()
        return context


class PhilosopherListView(ListView):
    model = Philosopher
    template_name = "content/philosopher_list.html"
    context_object_name = "philosophers"
    paginate_by = 10

    def get_queryset(self):
        return Philosopher.objects.select_related("era")


class PhilosopherDetailView(DetailView):
    model = Philosopher
    template_name = "content/philosopher_detail.html"
    context_object_name = "philosopher"

    def get_queryset(self):
        return Philosopher.objects.select_related("era")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["texts"] = self.object.texts.all()
        context["lessons"] = self.object.lessons.select_related(
            "course"
        ).filter(
            course__status=Course.Status.PUBLISHED
        )

        return context
