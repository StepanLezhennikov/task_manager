from rest_framework import serializers

from tasks.models import Task
from .models import Project, ProjectUser
from tasks.serializers import TaskSerializer, TaskForProjectSerializer


class ProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ['project',  'role']


class ProjectUserForProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ['user_id', 'user_email', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    project_users = ProjectUserForProjectSerializer(many=True, required=False)
    tasks = TaskForProjectSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['name', 'description', 'logo_url', 'project_users', 'tasks']

    def create(self, validated_data):
        name = validated_data.pop('name')
        description = validated_data.pop('description', None)
        logo_url = validated_data.pop('logo_url', None)

        project = Project.objects.create(name=name, description=description, logo_url=logo_url)

        for task in validated_data.pop('tasks', []):
            task = Task.objects.create(project=project, **task)
        for project_user in validated_data.pop('project_users', []):
            project_user = ProjectUser.objects.create(project=project, **project_user)

        return project

