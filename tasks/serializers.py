from rest_framework import serializers

from tasks.models import Task, TaskSubscription


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["project", "title", "description", "status", "deadline"]


class UpdateTaskDeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["deadline"]


class TaskForProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "deadline", "updated_at"]


class TaskSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSubscription
        fields = ["user_id", "task"]
