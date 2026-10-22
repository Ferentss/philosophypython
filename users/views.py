
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

from content.models import Course


def register(request):
    if request.user.is_authenticated:
        return redirect("users:dashboard")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("users:dashboard")
    else:
        form = UserCreationForm()

    return render(
        request,
        "users/register.html",
        {"form": form}
    )


@login_required
def dashboard(request):
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
        context
    )
