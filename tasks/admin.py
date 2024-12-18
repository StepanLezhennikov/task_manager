from django.contrib import admin

from .models import Task, TaskSubscription


class TaskAdmin(admin.ModelAdmin):
    pass


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskSubscription)