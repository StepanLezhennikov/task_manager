from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Task, TaskSubscription
from tasks.serializers import TaskSerializer, TaskSubscriptionSerializer
from .services import TaskService


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class UpdateTaskDeadlineView(APIView):
    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response("Задача не найдена", status=status.HTTP_404_NOT_FOUND)

        result = TaskService.update_deadline(task, request.data)
        if result["success"]:
            return Response(result["data"], status=status.HTTP_200_OK)
        return Response(result["errors"], status=status.HTTP_400_BAD_REQUEST)


class TaskSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = TaskSubscription.objects.all()
    serializer_class = TaskSubscriptionSerializer