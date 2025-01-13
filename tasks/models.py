from django.db import models

from projects.models import Project

from .validators import validate_deadline_in_future


class Task(models.Model):
    STATUS_CHOICES = [
        ("BACKLOG", "Backlog"),
        ("RUNNING", "Running"),
        ("DONE", "Done"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    deadline = models.DateTimeField(
        blank=True, null=True, validators=[validate_deadline_in_future]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskSubscription(models.Model):
    ROLE_CHOICES = [
        ("OWNER", "Owner"),
        ("PERFORMER", "Performer"),
        ("SUBSCRIBER", "Subscriber"),
    ]

    user_id = models.BigIntegerField()
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="subscriptions"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="PERFORMER")
    is_subscribed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("task", "user_id")

    def __str__(self):
        return f"User_id: {self.user_id} - task: {self.task}"
