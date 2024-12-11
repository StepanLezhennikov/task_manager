from django.db import models

from projects.models import Project


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField(blank=True, null=True)
    status = models.Choices('PENDING', 'RUNNING', 'DONE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title