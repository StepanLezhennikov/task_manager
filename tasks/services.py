from datetime import datetime

from rest_framework.generics import get_object_or_404

from tasks.models import Task
from tasks.schemas.dto import TaskDeadlineChangedResponse


class TaskService:
    @staticmethod
    def update_deadline(pk: int, deadline: datetime) -> TaskDeadlineChangedResponse:
        task = get_object_or_404(Task, pk=pk)
        task.deadline = deadline
        task.save()
        return TaskDeadlineChangedResponse(status="success", deadline=deadline)
