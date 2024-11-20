from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Habit, MorningRoutine, Task, EveningRoutine,DailyPlanner, Schedule, ToDoTask,WeeklyOverview
from .forms import MorningRoutineForm, TaskForm ,EveningTaskForm,ScheduleForm, ToDoTaskForm,HabitForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .models import Note
from django.contrib.auth import logout
from datetime import date


# Home View
def home(request):
    context = {
        "quote": "Indeed, with hardship comes ease. - Quran 94:6",
        "tasks": ["Morning Prayer", "Complete Homework", "Read Quran"],
        "quran_progress": {"chapters_read": 2, "daily_goal": 3},
    }
    return render(request, "home.html", context)

def toggle_task_completion(request, task_id):
       if request.method == 'POST':
           try:
               task = Task.objects.get(id=task_id)
               task.completed = not task.completed  # Toggle completion status
               task.save()
               return JsonResponse({'success': True})
           except Task.DoesNotExist:
               return JsonResponse({'success': False, 'error': 'Task not found.'})
       return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def morning_routine(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.category = "Morning"
            task.save()
            return redirect("morning_routine")

    tasks = Task.objects.filter(user=request.user, category="Morning").order_by("time")
    form = TaskForm()
    return render(request, "morning_routine.html", {"tasks": tasks, "form": form})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == "POST":
        task.delete()
        # Redirect the user to the previous page (or a different page) after the deletion
        return redirect('morning_routine')  # Replace 'tasks_list' with the appropriate URL name for the task list view.
    
    # If method is not POST, just redirect or show an error page.
    return redirect('morning_routine')  # Optionally redirect to another page or the task list view.


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            # Redirect after successfully updating the task
            return redirect('morning_routine')  # Redirect to task list (or another appropriate page)
    
    # If method is GET, render the edit form with the current task data
    form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'task': task})


# Daily Planner View

@login_required
def daily_planner(request):
    date_param = request.GET.get('date')
    planner_date = date.fromisoformat(date_param) if date_param else date.today()
    
    # Fetch or create the planner for the user and date
    planner, created = DailyPlanner.objects.get_or_create(user=request.user, date=planner_date)
    
    schedules = planner.schedules.all()
    tasks = planner.tasks.all()

    if request.method == 'POST':
        if 'add_schedule' in request.POST:
            schedule_form = ScheduleForm(request.POST)
            if schedule_form.is_valid():
                schedule = schedule_form.save(commit=False)
                schedule.planner = planner
                schedule.save()
                return redirect('daily_planner')
        elif 'add_task' in request.POST:
            task_form = ToDoTaskForm(request.POST)
            if task_form.is_valid():
                task = task_form.save(commit=False)
                task.planner = planner
                task.save()
                return redirect('daily_planner')
    else:
        schedule_form = ScheduleForm()
        task_form = ToDoTaskForm()

    return render(request, 'daily_planner.html', {
        'schedules': schedules,
        'tasks': tasks,
        'schedule_form': schedule_form,
        'task_form': task_form,
        'planner_date': planner_date,
    })

@login_required
def toggle_schedule_completion(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    schedule.completed = not schedule.completed
    schedule.save()
    return JsonResponse({'completed': schedule.completed})

@login_required
def toggle_task_completion(request, task_id):
    task = ToDoTask.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return JsonResponse({'completed': task.completed})

@login_required
def delete_schedule(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    schedule.delete()
    return redirect('daily_planner')

@login_required
def delete_task(request, task_id):
    task = ToDoTask.objects.get(id=task_id)
    task.delete()
    return redirect('daily_planner')

# Evening Routine View

@login_required
def evening_routine(request):
    # Fetch tasks for the current user
    routines = EveningRoutine.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = EveningTaskForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.user = request.user  # Ensure task is associated with the logged-in user
            routine.save()
            return redirect('evening_routine')  # Redirect after saving the task
    else:
        form = EveningTaskForm()

    # Pass tasks and form to the template
    return render(request, "evening_routine.html", {"tasks": routines, "form": form})
@login_required
def edit_evening_task(request, task_id):
    task = get_object_or_404(EveningRoutine, id=task_id, user=request.user)
    
    if request.method == 'POST':
        form = EveningTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('evening_routine')
    else:
        form = EveningTaskForm(instance=task)
    
    return render(request, 'edit_evening_task.html', {'form': form, 'task': task})

@login_required
def delete_evening_task(request, task_id):
    task = get_object_or_404(EveningRoutine, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('evening_routine')

# Weekly Overview View

@login_required
def weekly_overview(request):
    weekly_overview_data = WeeklyOverview.objects.filter(user=request.user).order_by('week_start_date')
    
    context = {
        'weekly_overview_data': weekly_overview_data
    }
    return render(request, 'weekly_overview.html')

# Habit Tracker View
@login_required
def habit_tracker(request):
    # Retrieve habits related to the logged-in user
    habits = Habit.objects.filter(user=request.user)
    
    # Initialize the form for GET requests or bind the POST data for POST requests
    if request.method == 'POST':
        form = HabitForm(request.POST)
        
        # If the form is valid, save the habit and redirect to the habit tracker page
        if form.is_valid():
            habit = form.save(commit=False)  # Save the habit instance without committing to the database
            habit.user = request.user  # Set the user to the current logged-in user
            habit.save()  # Commit the habit to the database
            return redirect('habit_tracker')  
        else:
            print(form.errors)
           # Redirect to the same page
    else:
        form = HabitForm()  # Initialize an empty form for GET requests

    # Render the template with the habits and the form
    return render(request, 'habit_tracker.html', {'habits': habits, 'form': form})

    
def mark_completed(request, habit_id):
    habit = Habit.objects.get(id=habit_id)
    habit.completed_days += 1
    habit.save()
    return redirect('habit_tracker')  # Redirect back to the habit tracker page
# Notes View
def notes(request):
    context = {
        "notes": [
            {"title": "Meeting Notes", "content": "Discuss project timeline", "date": "Nov 18"},
            {"title": "Reminder", "content": "Buy groceries", "date": "Nov 17"},
        ]
    }
    return render(request, "notes.html", context)




# Create your views here.
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Associate task with the logged-in user
            task.save()
            return redirect('daily_planner')  # Redirect to the planner page
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == "POST":
        note.delete()
        return redirect('notes')
    return render(request, 'confirm_delete.html', {'note': note})


def notes(request):
    notes_list = Note.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(notes_list, 5)  # Show 5 notes per page

    page_number = request.GET.get('page')
    notes = paginator.get_page(page_number)

    return render(request, 'notes.html', {'notes': notes})



def landing(request):
    return render(request, 'landing.html')



# Sign-Up View


@login_required
def dashboard(request):
    # Here, you would pass the user's tasks from the database
    return render(request, 'dashboard.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()

            # Log the user in immediately
            login(request, user)

            # Redirect the user to the dashboard after successful signup
            return redirect('dashboard')  # Make sure 'dashboard' matches the name of your dashboard view
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})



def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Authenticate and login the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log the user in
                login(request, user)
                # Redirect to the dashboard after successful login
                return redirect('dashboard')
            else:
                # Invalid login, return an error message
                form.add_error(None, "Invalid username or password")
        else:
            form = AuthenticationForm()

    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    # Log out the user
    logout(request)
    
    # Redirect the user to the landing page (or home page)
    return redirect('landing')