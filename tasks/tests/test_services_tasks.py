import pytest

from tasks.models import Task
from tasks.services import TaskService


@pytest.mark.django_db
def test_update_task_deadline_service(task_data_views):
    """Тест обновления срока выполнения задачи через TaskService."""

    task = Task.objects.create(
        title=task_data_views["title"],
        description=task_data_views["description"],
        project_id=task_data_views["project"],
        status=task_data_views["status"],
        deadline=task_data_views["deadline"],
    )

    new_deadline = "2025-01-01T00:00:00Z"
    result = TaskService.update_deadline(task.pk, {"deadline": new_deadline})

    assert result.status == "success"
    assert result.deadline == new_deadline

    task.refresh_from_db()
    assert task.deadline.isoformat().replace("+00:00", "Z") == new_deadline


@pytest.mark.django_db
def test_update_task_deadline_service_task_not_found(task_data_views):
    """Тест ошибки при отсутствии задачи с указанным ID."""

    invalid_task_id = 99999
    new_deadline = "2025-01-01T00:00:00Z"
    result = TaskService.update_deadline(invalid_task_id, {"deadline": new_deadline})
    assert result.status == "error"
    assert result.error == "Incorrect task Id"


@pytest.mark.django_db
def test_update_task_deadline_service_invalid_deadline(task_data_views):
    """Тест ошибки при некорректном формате даты."""

    task = Task.objects.create(
        title=task_data_views["title"],
        description=task_data_views["description"],
        project_id=task_data_views["project"],
        status=task_data_views["status"],
        deadline=task_data_views["deadline"],
    )

    invalid_deadline = "invalid-date-format"
    result = TaskService.update_deadline(task.pk, {"deadline": invalid_deadline})

    assert result.status == "error"
    assert result.error == "Incorrect deadline"
