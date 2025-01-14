from django.db import models
from django.utils.translation import gettext_lazy as _

from projects.models import Project
from tasks.validators import validate_deadline_in_future


class Task(models.Model):
    class Status(models.TextChoices):
        BACKLOG = "BACKLOG", _("Backlog")
        RUNNING = "RUNNING", _("Running")
        DONE = "DONE", _("Done")

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.BACKLOG
    )
    deadline = models.DateTimeField(
        blank=True, null=True, validators=[validate_deadline_in_future]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskSubscription(models.Model):
    class RoleChoices(models.TextChoices):
        OWNER = "OWNER", _("Owner")
        PERFORMER = "PERFORMER", _("Performer")
        SUBSCRIBER = "SUBSCRIBER", _("Subscriber")

    user_id = models.BigIntegerField()
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="subscriptions"
    )
    role = models.CharField(
        max_length=10, choices=RoleChoices.choices, default=RoleChoices.PERFORMER
    )
    is_subscribed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("task", "user_id")

    def __str__(self):
        return f"User_id: {self.user_id} - task: {self.task}"
