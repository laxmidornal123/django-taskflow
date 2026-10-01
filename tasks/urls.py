from django.urls import path

from . import views


urlpatterns = [

    # Authentication
    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # Dashboard
    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    # Tasks
    path(
        "task/create/",
        views.create_task,
        name="create_task"
    ),

    path(
        "task/<int:task_id>/edit/",
        views.edit_task,
        name="edit_task"
    ),

    path(
        "task/<int:task_id>/delete/",
        views.delete_task,
        name="delete_task"
    ),

    path(
        "task/<int:task_id>/toggle/",
        views.toggle_task,
        name="toggle_task"
    ),
]