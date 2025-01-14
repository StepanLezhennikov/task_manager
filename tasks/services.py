from datetime import datetime

from tasks.models import Task
from tasks.schemas.dto import TaskDeadlineChangedResponse


class TaskService:
    @staticmethod
    def update_deadline(pk: int, deadline: datetime) -> TaskDeadlineChangedResponse:
        try:
            task = Task.objects.get(pk=pk)
            task.deadline = deadline
            task.save()
            return TaskDeadlineChangedResponse(status="success", deadline=deadline)
        except Task.DoesNotExist:
            return TaskDeadlineChangedResponse(
                status="error", error="Incorrect task Id"
            )
        except Exception:
            return TaskDeadlineChangedResponse(
                status="error", error="Incorrect deadline"
            )
