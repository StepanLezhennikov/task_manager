from rest_framework import serializers

from projects.models import Project, ProjectUser
from tasks.serializers import TaskForProjectSerializer


class ProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ["project", "role"]


class GetProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ["user_id", "user_email", "role"]


class ProjectUserForProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ["user_id", "user_email", "role"]


class ProjectSerializer(serializers.ModelSerializer):
    project_users = ProjectUserForProjectSerializer(many=True, required=False)
    tasks = TaskForProjectSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ["name", "description", "logo_url", "project_users", "tasks"]
