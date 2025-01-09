import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from projects.models import Project, ProjectUser


@pytest.fixture
def api_client():
    """Фикстура для API клиента."""
    client = APIClient()
    return client


@pytest.fixture
def project():
    """Фикстура для создания проекта."""
    return Project.objects.create(
        name="Test Project",
        description="Test Description",
        logo_url="http://example.com/logo.png"
    )


@pytest.fixture
def project_user(project):
    """Фикстура для создания пользователя в проекте."""
    return ProjectUser.objects.create(
        project=project,
        user_id=1,
        user_email="stepanlezennikov@gmail.com",
        role="editor"
    )


@pytest.fixture
def project_data():
    """Данные для создания проекта через API."""
    return {
        "name": "Test Project",
        "description": "Test Description",
        "logo_url": "http://example.com/logo.png"
    }


@pytest.fixture
def invalid_project_data():
    """Неправильные данные для создания проекта через API."""
    return {
        "name": "",
        "description": "Test Description",
        "logo_url": "INVALID URL"
    }
