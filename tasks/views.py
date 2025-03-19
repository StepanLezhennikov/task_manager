import logging
from datetime import datetime

from rest_framework import status, viewsets
from dateutil.parser import ParserError, parse
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api.auth import AuthAPI
from tasks.models import Task, TaskSubscription
from tasks.filters import TaskFilter
from tasks.services import TaskService
from tasks.permissions import IsTaskOwner, IsTaskPerformer, IsSafeMethodPermission
from tasks.serializers import TaskSerializer, TaskSubscriptionSerializer
from api.kafka_producer import TOPICS, KafkaProducerService
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
    permission_classes = [IsSafeMethodPermission | IsTaskPerformer | IsTaskOwner]

    def perform_create(self, serializer):
        task = serializer.save()
        TaskSubscription.objects.create(
            task=task,
            user_id=self.request.user_data.id,
            role=TaskSubscription.RoleChoices.OWNER,
            is_subscribed=True,
        )
        user_email = AuthAPI.get_email_by_id(self.request.user_data.id)
        NotificationService.send_deadline_notification(
            task.id, task.deadline, [user_email]
        )
        KafkaProducerService().send_message(
            {
                "task_id": task.id,
                "project_id": task.project.pk,
                "status": task.status,
                "deadline": task.deadline.isoformat(),
                "owner_id": self.request.user_data.id,
                "created_at": datetime.now().isoformat(),
            },
            TOPICS.TASK_CREATED.value,
        )

    def perform_destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        NotificationService.remove_deadline_tasks(
            instance.id, matching_task_deadline=instance.deadline
        )

        KafkaProducerService().send_message(
            {
                "task_id": instance.id,
                "project_id": instance.project.pk,
                "created_at": datetime.now().isoformat(),
            },
            TOPICS.TASK_DELETED.value,
        )

        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()

        response = super().update(request, *args, **kwargs)
        instance.refresh_from_db()

        KafkaProducerService().send_message(
            {
                "task_id": instance.id,
                "project_id": instance.project.pk,
                "user_id": self.request.user_data.id,
                "status": instance.status,
                "task_started_time": instance.created_at.isoformat(),
                "created_at": datetime.now().isoformat(),
            },
            TOPICS.TASK_UPDATED.value,
        )

        return response


class UpdateTaskDeadlineView(APIView):
    permission_classes = [IsTaskOwner | IsTaskPerformer]

    def patch(self, request, **kwargs):
        pk = self.kwargs.get("pk")
        try:
            new_deadline = parse(request.data.get("deadline"))
        except ParserError:
            return Response(
                {"error": "Invalid date format. Please use YYYY-MM-DD format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = TaskService.update_deadline(pk, new_deadline)
        if result.status == "success":
            user_email = AuthAPI.get_email_by_id(self.request.user_data.id)
            NotificationService.send_deadline_notification_after_changing_deadline(
                pk, new_deadline, [user_email]
            )
            return Response({"deadline": result.deadline}, status=status.HTTP_200_OK)
        return Response(result.error, status=status.HTTP_400_BAD_REQUEST)


class TaskSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = TaskSubscription.objects.all()
    serializer_class = TaskSubscriptionSerializer
