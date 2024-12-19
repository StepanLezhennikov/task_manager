import pytest
from django.utils.dateparse import parse_datetime

from tasks.models import Task, TaskSubscription
from tasks.serializers import (
    TaskSerializer,
    UpdateTaskDeadlineSerializer,
    TaskForProjectSerializer,
    TaskSubscriptionSerializer,
)


@pytest.mark.django_db
def test_task_serializer_valid_data(task_data_serializers, project):
    """Тест сериализации задачи с валидными данными."""
    serializer = TaskSerializer(data=task_data_serializers)
    assert serializer.is_valid(), f"Ошибки сериализации: {serializer.errors}"
    task = serializer.save()
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "BACKLOG"
    assert task.project == project


@pytest.mark.django_db
def test_task_serializer_invalid_data(invalid_task_data):
    """Тест сериализации задачи с невалидными данными."""
    serializer = TaskSerializer(data=invalid_task_data)
    assert not serializer.is_valid()
    assert "project" in serializer.errors
    assert "status" in serializer.errors


@pytest.mark.django_db
def test_update_task_deadline_serializer(task_data_serializers):
    """Тест обновления срока выполнения задачи."""
    task = Task.objects.create(
        title="Initial Task",
        description="Initial Description",
        project_id=task_data_serializers["project"],
        status="BACKLOG",
        deadline="2024-12-20T00:00:00Z",
    )

    updated_data = {"deadline": "2025-01-01T00:00:00Z"}
    serializer = UpdateTaskDeadlineSerializer(instance=task, data=updated_data, partial=True)
    assert serializer.is_valid(), f"Ошибки сериализации: {serializer.errors}"
    updated_task = serializer.save()
    expected_deadline = parse_datetime(updated_data["deadline"])
    assert updated_task.deadline == expected_deadline, (
        f"Ожидаемое значение: {expected_deadline}, полученное: {updated_task.deadline}"
    )

@pytest.mark.django_db
def test_task_for_project_serializer(task_data_serializers):
    """Тест сериализации задачи для отображения в проекте."""
    deadline = parse_datetime(task_data_serializers["deadline"])

    task = Task.objects.create(
        title=task_data_serializers["title"],
        description=task_data_serializers["description"],
        project_id=task_data_serializers["project"],
        status=task_data_serializers["status"],
        deadline=deadline,
    )

    serializer = TaskForProjectSerializer(instance=task)

    expected_data = {
        "title": task_data_serializers["title"],
        "description": task_data_serializers["description"],
        "status": task_data_serializers["status"],
        "deadline": task.deadline.isoformat().replace('+00:00', 'Z'),
        "updated_at": task.updated_at.isoformat().replace('+00:00', 'Z'),
    }

    assert serializer.data == expected_data, (
        f"Ожидаемые данные: {expected_data}, Полученные данные: {serializer.data}"
    )


@pytest.mark.django_db
def test_task_subscription_serializer(project):
    """Тест сериализации подписки на задачу."""
    task = Task.objects.create(
        title="Subscribed Task",
        description="Task with subscription",
        project=project,
        status="BACKLOG",
        deadline="2024-12-31T00:00:00Z",
    )
    subscription = TaskSubscription.objects.create(user_id=1, task=task)

    serializer = TaskSubscriptionSerializer(instance=subscription)
    expected_data = {
        "user_id": 1,
        "task": task.id,
    }
    assert serializer.data == expected_data
