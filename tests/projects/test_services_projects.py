import pytest

from projects.models import ProjectUser
from projects.services import ProjectService


@pytest.mark.django_db
def test_get_project_users(project, project_user):
    """Test retrieving project users."""
    users = ProjectService.get_project_users(project.id)
    assert len(users) == 2
    assert users[0]["user_id"] == project.project_users.first().id
    assert users[0]["role"] == project.project_users.first().role
    assert users[1]["user_id"] == project_user.id
    assert users[1]["role"] == project_user.role


@pytest.mark.django_db
def test_get_project_name_by_id(project):
    """Test retrieving project name by ID."""
    name = ProjectService.get_project_name_by_id(project.id)
    assert name == project.name


@pytest.mark.django_db
def test_create_project_with_users_and_tasks():
    """Test creating a project with users and tasks."""
    project_data = {
        "name": "Test Project data",
        "description": "Test Description data",
        "logo_url": "http://example.com/logo.png",
    }
    project_data_test = project_data.copy()
    project = ProjectService.create_project_with_users_and_tasks(project_data, 50)
    assert project.name == project_data_test["name"]
    assert project.description == project_data_test["description"]
    assert ProjectUser.objects.filter(project=project, user_id=50).exists()
