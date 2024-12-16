from .serializers import UpdateTaskDeadlineSerializer


class TaskService:
    @staticmethod
    def update_deadline(task, data):
        serializer = UpdateTaskDeadlineSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return {"success": True, "data": serializer.data}
        return {"success": False, "errors": serializer.errors}
