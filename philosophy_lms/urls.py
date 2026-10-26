from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    path("users/", include("users.urls")),

    path(
        "social-auth/",
        include("social_django.urls", namespace="social"),
    ),

    path("", include("content.urls")),
]
