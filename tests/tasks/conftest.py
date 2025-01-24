from datetime import datetime, timedelta

import pytest
from django.utils import timezone

from tasks.models import Task, TaskSubscription
from projects.models import Project, ProjectUser

TASKS_URL = "/api/v1/tasks/"
TASK_SUBSCRIPTIONS_URL = "/api/v1/task_subscriptions/"


@pytest.fixture
@pytest.mark.django_db
def project():
    """Фикстура для создания проекта."""
    project = Project.objects.create(
        name="Test Project",
        description="Test Description",
        logo_url="http://example.com/logo.png",
    )
    ProjectUser.objects.create(
        project=project,
        user_id=1,
        role=ProjectUser.RoleChoices.OWNER,
    )
    return project


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
        "deadline": datetime.now() + timedelta(days=3),
    }


@pytest.fixture
def task(project):
    """Создание задачи."""
    task = Task.objects.create(
        project=project,
        title="Write tests",
        description="Write unit tests for the application.",
        status=Task.Status.BACKLOG,
        deadline=datetime.now() + timedelta(days=3),
    )
    TaskSubscription.objects.create(
        user_id=1,
        task=task,
        role=TaskSubscription.RoleChoices.OWNER,
        is_subscribed=True,
    )
    return task


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
    return tasks
