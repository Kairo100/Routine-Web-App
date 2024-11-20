from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("", views.landing, name="landing"),
    path("home/", views.home, name="home"),
    path("morning-routine/", views.morning_routine, name="morning_routine"),
    path('morning-routine/toggle/<int:task_id>/', views.toggle_task_completion, name='toggle_task_completion'),
    path('morning-routine/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('morning-routine/edit-task/<int:task_id>/', views.update_task, name='edit_task'),
    path("daily-planner/", views.daily_planner, name="daily_planner"),
    path('schedule/<int:schedule_id>/toggle-completion/', views.toggle_schedule_completion, name='toggle_schedule_completion'),
    path('task/<int:task_id>/toggle-completion/', views.toggle_task_completion, name='toggle_task_completion'),
    path('schedule/<int:schedule_id>/delete/', views.delete_schedule, name='delete_schedule'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path("evening-routine/", views.evening_routine, name="evening_routine"),
    path('evening-routine/toggle/<int:task_id>/', views.edit_evening_task, name='edit_evening_task'),
    path('evening-routine/delete/<int:task_id>/', views.delete_evening_task, name='delete_evening_task'),
    path("weekly-overview/", views.weekly_overview, name="weekly_overview"),
    path("habit-tracker/", views.habit_tracker, name="habit_tracker"),
    path("habit-tracker/mark-complete/<int:habit_id>/", views.mark_completed, name='mark_completed'),
    path("notes/", views.notes, name="notes"),
    path('add-task/', views.add_task, name='add_task'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),  # Handle logout

]
