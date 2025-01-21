import pytest

from projects.models import Project, ProjectUser


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
