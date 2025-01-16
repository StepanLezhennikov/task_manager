from rest_framework import serializers

from projects.models import Project, ProjectUser
from tasks.serializers import TaskForProjectSerializer


class ProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ["project", "role"]


class ProjectUserSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ["user_id", "role"]


class ProjectSerializer(serializers.ModelSerializer):
    project_users = ProjectUserSerializerGet(many=True, required=False)
    tasks = TaskForProjectSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ["name", "description", "logo_url", "project_users", "tasks"]
