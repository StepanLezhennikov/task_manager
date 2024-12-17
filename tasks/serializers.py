from rest_framework import serializers
from .models import Task, TaskSubscription


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'status', 'deadline']

    # def create(self, validated_data: dict):
    #     deadline = validated_data.get('deadline')
    #     if deadline:
    #         # Отправка сообщения через Celery
    #         pass
    #     task = Task.objects.create(**validated_data)
    #     return task

class UpdateTaskDeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['deadline']

class TaskForProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'updated_at']


class TaskSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSubscription
        fields = ['user_id', 'task']
