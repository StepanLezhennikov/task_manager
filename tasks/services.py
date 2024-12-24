from .models import Task
from tasks.schemas.dto import TaskDeadlineChanged


class TaskService:
    @staticmethod
    def update_deadline(pk, data):
        try:
            task = Task.objects.get(pk=pk)
            task.deadline = data["deadline"]
            task.save()
            return TaskDeadlineChanged(status="success", deadline=data["deadline"])
        except Task.DoesNotExist:
            return TaskDeadlineChanged(status="error", error="Incorrect task Id")
        except:
            return TaskDeadlineChanged(status="error", error="Incorrect deadline")
