from django.contrib import admin
from .models import Task, Note, Habit,MorningRoutine,ToDoTask,Schedule,WeeklyOverview

admin.site.register(Task)
admin.site.register(Note)
admin.site.register(Habit)
admin.site.register(MorningRoutine)
admin.site.register(ToDoTask)
admin.site.register(Schedule)
admin.site.register(WeeklyOverview)

