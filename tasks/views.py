from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, RegisterForm, TaskForm
from .models import Task


# =========================================================
# USER REGISTRATION
# =========================================================

def register_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Account created successfully. Welcome!"
            )

            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(
        request,
        "tasks/register.html",
        {"form": form}
    )


# =========================================================
# USER LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    f"Welcome back, {user.username}!"
                )

                return redirect("dashboard")

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "tasks/login.html",
        {"form": form}
    )


# =========================================================
# USER LOGOUT
# =========================================================

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    tasks = Task.objects.filter(
        user=request.user
    )

    total_tasks = tasks.count()

    completed_tasks = tasks.filter(
        status="COMPLETED"
    ).count()

    pending_tasks = tasks.filter(
        status="PENDING"
    ).count()

    high_priority_tasks = tasks.filter(
        priority="HIGH"
    ).count()

    context = {
        "tasks": tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "high_priority_tasks": high_priority_tasks,
    }

    return render(
        request,
        "tasks/dashboard.html",
        context
    )


# =========================================================
# CREATE TASK
# =========================================================

@login_required
def create_task(request):

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)

            task.user = request.user

            task.save()

            messages.success(
                request,
                "Task created successfully!"
            )

            return redirect("dashboard")

    else:

        form = TaskForm()

    return render(
        request,
        "tasks/task_form.html",
        {
            "form": form,
            "page_title": "Create Task"
        }
    )


# =========================================================
# EDIT TASK
# =========================================================

@login_required
def edit_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if request.method == "POST":

        form = TaskForm(
            request.POST,
            instance=task
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Task updated successfully!"
            )

            return redirect("dashboard")

    else:

        form = TaskForm(
            instance=task
        )

    return render(
        request,
        "tasks/task_form.html",
        {
            "form": form,
            "page_title": "Edit Task"
        }
    )


# =========================================================
# DELETE TASK
# =========================================================

@login_required
def delete_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if request.method == "POST":

        task.delete()

        messages.success(
            request,
            "Task deleted successfully!"
        )

        return redirect("dashboard")

    return render(
        request,
        "tasks/task_confirm_delete.html",
        {
            "task": task
        }
    )


# =========================================================
# TOGGLE TASK STATUS
# =========================================================

@login_required
def toggle_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if task.status == "PENDING":

        task.status = "COMPLETED"

    else:

        task.status = "PENDING"

    task.save()

    return redirect("dashboard")

