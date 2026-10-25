
from django.urls import path
from django.views.generic import ListView, DetailView

from . import views
from .models import Era, Philosopher
from .text_views import TextListView, TextDetailView
from .lesson_views import LessonListView, LessonDetailView


app_name = "content"


urlpatterns = [
    # Головна сторінка
    path(
        "",
        views.home,
        name="home",
    ),

    # Філософські епохи
    path(
        "eras/",
        ListView.as_view(
            model=Era,
            template_name="content/era_list.html",
            context_object_name="eras",
            ordering=["start_year"],
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

    # Філософи
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

    # Філософські праці
    path(
        "texts/",
        TextListView.as_view(),
        name="text_list",
    ),

    path(
        "texts/<int:pk>/",
        TextDetailView.as_view(),
        name="text_detail",
    ),

    # Курси
    path(
        "courses/",
        views.course_list,
        name="course_list",
    ),

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

    # Список усіх доступних уроків
    path(
        "lessons/",
        LessonListView.as_view(),
        name="lesson_list",
    ),

    # Створення уроку для курсу
    path(
        "courses/<int:course_pk>/lessons/create/",
        views.LessonCreateView.as_view(),
        name="lesson_create",
    ),

    # Перегляд уроку
    path(
        "courses/<int:course_pk>/lessons/<int:lesson_pk>/",
        LessonDetailView.as_view(),
        name="lesson_detail",
    ),

    # Редагування уроку
    path(
        "lessons/<int:pk>/edit/",
        views.LessonUpdateView.as_view(),
        name="lesson_update",
    ),

    # Видалення уроку
    path(
        "lessons/<int:pk>/delete/",
        views.LessonDeleteView.as_view(),
        name="lesson_delete",
    ),
]
