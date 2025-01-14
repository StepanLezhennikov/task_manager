import logging

from rest_framework import status, viewsets
from dateutil.parser import parse
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from tasks.models import Task, TaskSubscription
from tasks.filters import TaskFilter
from tasks.services import TaskService
from tasks.permissions import IsTaskPerformerOrOwner, IsUserOwnerOrEditorOfProject
from tasks.serializers import TaskSerializer, TaskSubscriptionSerializer
from notifications.services import NotificationService

logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["title", "status"]
    filterset_class = TaskFilter
    ordering_fields = ["title", "created_at"]
    ordering = ["-created_at"]
    permission_classes = [IsTaskPerformerOrOwner, IsUserOwnerOrEditorOfProject]

    def perform_create(self, serializer):
        task = serializer.save()
        TaskSubscription.objects.create(
            task=task, user_id=self.request.user_id, role="Owner", is_subscribed=True
        )

        NotificationService.send_deadline_notification(
            task.id, task.deadline, ["stepanlezennikov@gmail.com"]
        )

    def perform_destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            NotificationService.remove_deadline_tasks(
                instance.id, matching_task_deadline=instance.deadline
            )
        except Exception as e:
            logger.error(
                f"Failed to remove Celery tasks for task ID: {instance.id}. Error: {str(e)}"
            )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateTaskDeadlineView(APIView):
    permission_classes = [IsTaskPerformerOrOwner]

    def patch(self, request, **kwargs):
        pk = self.kwargs.get("pk")
        new_deadline = parse(request.data.get("deadline"))

        result = TaskService.update_deadline(pk, new_deadline)
        if result.status == "success":
            NotificationService.send_deadline_notification_after_changing_deadline(
                pk, new_deadline, [self.request.user_email]
            )
            return Response({"deadline": result.deadline}, status=status.HTTP_200_OK)
        return Response(result.error, status=status.HTTP_400_BAD_REQUEST)


class TaskSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = TaskSubscription.objects.all()
    serializer_class = TaskSubscriptionSerializer
