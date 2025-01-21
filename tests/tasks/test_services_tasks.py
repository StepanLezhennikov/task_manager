from datetime import datetime, timedelta

import pytest
from django.http import Http404

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

    new_deadline = datetime.now() + timedelta(days=1)
    result = TaskService.update_deadline(task.pk, new_deadline)

    assert result.status == "success"
    assert result.deadline == new_deadline

    task.refresh_from_db()
    assert task.deadline.replace(tzinfo=None) == new_deadline.replace(tzinfo=None)  #


@pytest.mark.django_db
def test_update_task_deadline_service_task_not_found(task_data_views):
    """Тест ошибки при отсутствии задачи с указанным ID."""

    invalid_task_id = 99999
    new_deadline = datetime.now() + timedelta(days=1)
    try:
        TaskService.update_deadline(invalid_task_id, new_deadline)
    except Http404:
        assert True
