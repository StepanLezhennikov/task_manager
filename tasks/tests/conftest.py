import pytest
from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APIClient
from projects.models import Project
from tasks.models import Task

TASKS_URL = "/api/tasks/"
TASK_SUBSCRIPTIONS_URL = "/api/task_subscriptions/"

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def project():
    """Создание проекта для тестов."""
    return Project.objects.create(
        name="Test Project",
        description="Test Description",
    )


@pytest.fixture
def task_data_serializers(project):
    """Данные для проверки сериалайзеров."""
    return {
        "title": "Test Task",
        "description": "Test Description",
        "project": project.pk,
        "status": "BACKLOG",
        "deadline": "2024-12-31T23:59:59Z",
    }


@pytest.fixture
def task_data_views(project):
    """Данные для проверки views."""
    return {
        "project": project.pk,
        "title": "Write tests",
        "description": "Write unit tests for the application.",
        "status": "RUNNING",
        "deadline": "2024-12-27T00:00:00Z",
    }


@pytest.fixture
def invalid_task_data(project):
    """Неверные данные задачи."""
    return {
        "title": "Test Task",
        "project": "non-existent-id",
        "status": "INVALID_STATUS",
    }


@pytest.fixture
def task_data_filters(project):
    """Создание нескольких задач для тестирования фильтров."""
    now = timezone.now()

    tasks = [
        Task.objects.create(
            project=project,
            title="Write tests",
            description="Write unit tests for the application.",
            status="BACKLOG",
            deadline=now + timedelta(days=3),
        ),
        Task.objects.create(
            project=project,
            title="Deploy app",
            description="Deploy the app to production.",
            status="RUNNING",
            deadline=now + timedelta(days=5),
            created_at=now - timedelta(days=1),
        ),
        Task.objects.create(
            project=project,
            title="Fix app bugs",
            description="Fix critical bugs in the app.",
            status="DONE",
            deadline=now + timedelta(days=7),
            created_at=now - timedelta(days=2),
        ),
    ]
    return Task.objects.all()
