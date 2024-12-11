from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name="Project Name")
    description = models.TextField(blank=True, verbose_name="Project Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
