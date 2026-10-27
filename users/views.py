
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from content.models import Course
from .forms import CustomUserCreationForm


def register(request):
    # Якщо користувач уже увійшов у систему
    if request.user.is_authenticated:
        return redirect("users:dashboard")

    # Обробка форми реєстрації
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Автоматичний вхід після реєстрації
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")

            return redirect("users:dashboard")

    else:
        form = CustomUserCreationForm()

    return render(
        request,
        "users/register.html",
        {"form": form},
    )


@login_required
def dashboard(request):
    # Отримуємо тільки власні курси користувача
    courses = Course.objects.filter(
        owner=request.user
    ).order_by("-created_at")

    context = {
        "courses": courses,
        "total_courses": courses.count(),
    }

    return render(
        request,
        "users/dashboard.html",
        context,
    )
