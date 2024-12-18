from django.contrib import admin

from .models import Project, ProjectUser


class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectUser)
