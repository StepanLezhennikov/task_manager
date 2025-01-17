from typing import Dict

import pytest
from jose import jwt
from rest_framework.test import APIClient

from projects.models import Project, ProjectUser
from projects.schemas.dto import Role


def create_jwt_token(user_id: int | None = None, role: Role | None = None) -> str:
    payload = {}
    if user_id is not None:
        payload.update({"id": str(user_id)})
    if role is not None:
        payload.update({"role": str(role)})
    return jwt.encode(payload, "super_secret_key", algorithm="HS256")


@pytest.fixture
def api_client():
    """Фикстура для API клиента."""
    client = APIClient()
    return client


@pytest.fixture
def admin_headers() -> Dict[str, str]:
    return {"Authorization": create_jwt_token(user_id=1, role=Role.ADMIN)}


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
@pytest.mark.django_db
def project_user(project):
    """Фикстура для создания пользователя в проекте."""
    return ProjectUser.objects.create(
        project=project,
        user_id=2,
        role=ProjectUser.RoleChoices.EDITOR,
    )


@pytest.fixture
def project_data():
    """Данные для создания проекта через API."""
    return {
        "name": "Test Project data",
        "description": "Test Description data",
        "logo_url": "http://example.com/logo.png",
    }


@pytest.fixture
def invalid_project_data():
    """Неправильные данные для создания проекта через API."""
    return {"name": "", "description": "Test Description", "logo_url": "INVALID URL"}
