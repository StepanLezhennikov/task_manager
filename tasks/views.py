from rest_framework import viewsets

from tasks.models import Task, TaskSubscription
from tasks.serializers import TaskSerializer, TaskSubscriptionSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = TaskSubscription.objects.all()
    serializer_class = TaskSubscriptionSerializer