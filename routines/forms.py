from django import forms
from .models import Task, Habit, Note, MorningRoutine,EveningRoutine, Schedule, ToDoTask,Habit




class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "time", "completed"]
        widgets = {
            "time": forms.TimeInput(attrs={"type": "time"}),
        }

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'days_to_complete', 'start_date']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class MorningRoutineForm(forms.ModelForm):
    class Meta:
        model = MorningRoutine
        fields = ['wake_up_time', 'fajr_time', 'dhuhr_time', 'quran_chapters_read']
        widgets = {
            'wake_up_time': forms.TimeInput(attrs={'type': 'time'}),
            'fajr_time': forms.TimeInput(attrs={'type': 'time'}),
            'dhuhr_time': forms.TimeInput(attrs={'type': 'time'}),
            'quran_chapters_read': forms.NumberInput(attrs={'min': 0}),
        }


        
class EveningTaskForm(forms.ModelForm):
    class Meta:
        model = EveningRoutine
        fields = ['name', 'time', 'completed']
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})  # Ensures a time picker
        }


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['name', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class ToDoTaskForm(forms.ModelForm):
    class Meta:
        model = ToDoTask
        fields = ['task']
        widgets = {
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
