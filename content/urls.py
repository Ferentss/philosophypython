
from django.urls import path
from django.views.generic import DetailView, RedirectView

from . import views
from .models import Era, Philosopher

app_name = "content"

urlpatterns = [
    path("", views.home, name="home"),

    path(
        "eras/",
        RedirectView.as_view(
            url="/#epochs",
            permanent=False
        ),
        name="era_list",
    ),

    path(
        "eras/<int:pk>/",
        DetailView.as_view(
            model=Era,
            template_name="content/era_detail.html",
            context_object_name="era",
        ),
        name="era_detail",
    ),

    path(
        "philosophers/",
        views.philosopher_list,
        name="philosopher_list",
    ),

    path(
        "philosophers/<int:pk>/",
        DetailView.as_view(
            model=Philosopher,
            template_name="content/philosopher_detail.html",
            context_object_name="philosopher",
        ),
        name="philosopher_detail",
    ),

    path("courses/", views.course_list, name="course_list"),

    path(
        "courses/create/",
        views.CourseCreateView.as_view(),
        name="course_create",
    ),

    path(
        "courses/<int:pk>/",
        views.course_detail,
        name="course_detail",
    ),

    path(
        "courses/<int:pk>/edit/",
        views.CourseUpdateView.as_view(),
        name="course_update",
    ),

    path(
        "courses/<int:pk>/delete/",
        views.CourseDeleteView.as_view(),
        name="course_delete",
    ),

    path(
        "courses/<int:course_pk>/lessons/create/",
        views.LessonCreateView.as_view(),
        name="lesson_create",
    ),

    path(
        "courses/<int:course_pk>/lessons/<int:lesson_pk>/",
        views.lesson_detail,
        name="lesson_detail",
    ),

    path(
        "lessons/<int:pk>/edit/",
        views.LessonUpdateView.as_view(),
        name="lesson_update",
    ),

    path(
        "lessons/<int:pk>/delete/",
        views.LessonDeleteView.as_view(),
        name="lesson_delete",
    ),
]
