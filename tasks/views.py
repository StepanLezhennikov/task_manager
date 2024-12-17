from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from tasks.models import Task, TaskSubscription
from tasks.serializers import TaskSerializer, TaskSubscriptionSerializer
from .services import TaskService
from .filters import TaskFilter


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["title", "status"]
    filterset_class = TaskFilter
    ordering_fields = ['title', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        # Отправка сообщения через Celery
        serializer.save()


class UpdateTaskDeadlineView(APIView):
    def patch(self, request, **kwargs):
        pk = self.kwargs.get('pk')
        result = TaskService.update_deadline(pk, request.data)
        if result["success"]:
            return Response(result["data"], status=status.HTTP_200_OK)
        return Response(result["errors"], status=status.HTTP_400_BAD_REQUEST)


class TaskSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = TaskSubscription.objects.all()
    serializer_class = TaskSubscriptionSerializer
