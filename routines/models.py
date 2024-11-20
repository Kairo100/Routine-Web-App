from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Task(models.Model):
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    time = models.TimeField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Habit(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)  # Make sure this line exists
    days_to_complete = models.PositiveIntegerField()
    completed_days = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)  # Add this line if you want a description field

    def __str__(self):
        return self.name
class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class MorningRoutine(models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE)
       tasks = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, default=None)
       wake_up_time = models.TimeField(null=True, blank=True)
       fajr_time = models.TimeField(null=True, blank=True)
       dhuhr_time = models.TimeField(null=True, blank=True)
       quran_chapters_read = models.IntegerField(default=0)

       def __str__(self):
        return f"{self.user.username}'s Morning Routine on {self.date}"

class DailyPlanner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"Planner for {self.user.username} on {self.date}"

class Schedule(models.Model):
    planner = models.ForeignKey(DailyPlanner, related_name='schedules', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.name}: {self.start_time} - {self.end_time}"

class ToDoTask(models.Model):
    planner = models.ForeignKey(DailyPlanner, related_name='tasks', on_delete=models.CASCADE)
    task = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
           return self.task

    
class EveningRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    time = models.TimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name if self.name else "Evening Task"

    class Meta:
        ordering = ['time']



class WeeklyOverview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start_date = models.DateField()  # This is the new field
    tasks_completed = models.PositiveIntegerField()
    tasks_total = models.PositiveIntegerField()
    habits_completed = models.PositiveIntegerField()
    habits_total = models.PositiveIntegerField()

    def completion_percentage(self):
        return (self.tasks_completed / self.tasks_total) * 100 if self.tasks_total else 0

    def habit_percentage(self):
        return (self.habits_completed / self.habits_total) * 100 if self.habits_total else 0

    def __str__(self):
        return f"{self.title} - Week of {self.week_start_date}"

    class Meta:
        ordering = ['-week_start_date']

class HabitTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit = models.CharField(max_length=100)
    frequency = models.IntegerField()  # e.g., days per week

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
