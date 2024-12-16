from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from tasks.models import Task, TaskSubscription
from tasks.serializers import TaskSerializer, TaskSubscriptionSerializer, UpdateTaskDeadlineSerializer
from .filters import TaskFilter



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["title", "status"]
    filterset_class = TaskFilter
    ordering_fields = ['title', 'created_at']
    ordering = ['-created_at']


class UpdateTaskDeadlineView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = UpdateTaskDeadlineSerializer



class TaskSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = TaskSubscription.objects.all()
    serializer_class = TaskSubscriptionSerializer
