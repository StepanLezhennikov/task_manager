from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name="Project Name")
    description = models.TextField(blank=True, verbose_name="Project Description")
    logo_url = models.URLField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProjectUser(models.Model):
    ROLE_CHOICES = [
        ("reader", "Reader"),
        ("editor", "Editor"),
        ("owner", "Owner"),
    ]

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_users"
    )
    user_id = models.BigIntegerField()
    user_email = models.EmailField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="reader")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("project", "user_id")

    def __str__(self):
        return f"{self.user_email} ({self.role}) in {self.project.name}"
