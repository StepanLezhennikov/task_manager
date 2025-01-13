from tasks.schemas.dto import TaskDeadlineChanged

from .models import Task


class TaskService:
    @staticmethod
    def update_deadline(pk: int, data: TaskDeadlineChanged) -> TaskDeadlineChanged:
        try:
            task = Task.objects.get(pk=pk)
            task.deadline = data.deadline
            task.save()
            return TaskDeadlineChanged(status="success", deadline=data.deadline)
        except Task.DoesNotExist:
            return TaskDeadlineChanged(status="error", error="Incorrect task Id")
        except Exception:
            return TaskDeadlineChanged(status="error", error="Incorrect deadline")
