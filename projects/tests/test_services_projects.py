import pytest

from projects.models import ProjectUser
from projects.services import ProjectService


@pytest.mark.django_db
def test_get_project_users(project, project_user):
    """Test retrieving project users."""
    users = ProjectService.get_project_users(project.id)
    assert len(users) == 1
    assert users[0]["user_id"] == project_user.user_id
    assert users[0]["role"] == project_user.role


@pytest.mark.django_db
def test_get_project_name_by_id(project):
    """Test retrieving project name by ID."""
    name = ProjectService.get_project_name_by_id(project.id)
    assert name == project.name


@pytest.mark.django_db
def test_create_project_with_users_and_tasks(user, project_data):
    """Test creating a project with users and tasks."""
    project = ProjectService.create_project_with_users_and_tasks(project_data, user.id)
    assert project.name == project_data["name"]
    assert project.description == project_data["description"]
    assert ProjectUser.objects.filter(project=project, user_id=user.id).exists()
