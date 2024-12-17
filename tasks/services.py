from .models import Task
from .serializers import UpdateTaskDeadlineSerializer


class TaskService:
    @staticmethod
    def update_deadline(pk, data):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return {"success": False, "errors": "Задача не найдена"}
        serializer = UpdateTaskDeadlineSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Отправка сообщения через Celery
            # Удаление предыдущего запроса на отправку для этой таски
            return {"success": True, "data": serializer.data}
        return {"success": False, "errors": serializer.errors}
