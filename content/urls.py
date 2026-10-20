
from django.urls import path

from . import views


app_name = "content"

urlpatterns = [
    path(
        "",
        views.home,
        name="home"
    ),
    path(
        "courses/",
        views.CourseListView.as_view(),
        name="course_list"
    ),
    path(
        "courses/create/",
        views.CourseCreateView.as_view(),
        name="course_create"
    ),
    path(
        "courses/<int:pk>/",
        views.CourseDetailView.as_view(),
        name="course_detail"
    ),
    path(
        "courses/<int:pk>/edit/",
        views.CourseUpdateView.as_view(),
        name="course_update"
    ),
    path(
        "courses/<int:pk>/delete/",
        views.CourseDeleteView.as_view(),
        name="course_delete"
    ),
    path(
        "lessons/<int:pk>/",
        views.LessonDetailView.as_view(),
        name="lesson_detail"
    ),
    path(
        "eras/",
        views.EraListView.as_view(),
        name="era_list"
    ),
    path(
        "eras/<int:pk>/",
        views.EraDetailView.as_view(),
        name="era_detail"
    ),
    path(
        "philosophers/",
        views.PhilosopherListView.as_view(),
        name="philosopher_list"
    ),
    path(
        "philosophers/<int:pk>/",
        views.PhilosopherDetailView.as_view(),
        name="philosopher_detail"
    ),
]
