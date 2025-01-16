from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name="Project Name")
    description = models.TextField(blank=True, verbose_name="Project Description")
    logo_url = models.URLField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProjectUser(models.Model):
    class RoleChoices(models.TextChoices):
        READER = "reader", _("Reader")
        EDITOR = "editor", _("Editor")
        OWNER = "owner", _("Owner")

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_users"
    )
    user_id = models.BigIntegerField()
    role = models.CharField(
        max_length=10, choices=RoleChoices.choices, default=RoleChoices.READER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("project", "user_id")

    def __str__(self):
        return f"{self.user_id} ({self.role}) in {self.project.name}"
