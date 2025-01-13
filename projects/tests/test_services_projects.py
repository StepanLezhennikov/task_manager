import pytest
from projects.services import ProjectService
from projects.models import ProjectUser


@pytest.mark.django_db
def test_get_project_users(project, project_user):
    """Test retrieving the list of users in a project."""
    users = ProjectService.get_project_users(project.id)
    assert len(users) == 1
    assert users[0]["user_id"] == project_user.user_id
    assert users[0]["role"] == project_user.role


@pytest.mark.django_db
def test_get_project_users_empty(project):
    """Test retrieving an empty list if there are no users in the project."""
    users = ProjectService.get_project_users(project.id)
    assert users == []


@pytest.mark.django_db
def test_get_project_name_by_id(project):
    """Test retrieving the project name by its ID."""
    project_name = ProjectService.get_project_name_by_id(project.id)
    assert project_name == project.name


@pytest.mark.django_db
def test_get_project_name_by_id_nonexistent():
    """Test that None is returned if the project does not exist."""
    project_name = ProjectService.get_project_name_by_id(9999)
    assert project_name is None


@pytest.mark.django_db
def test_get_project_users_multiple(project, project_user):
    """Test retrieving multiple users in a project."""

    second_user = ProjectUser.objects.create(
        project=project, user_id=2, user_email="second@example.com", role="owner"
    )

    users = ProjectService.get_project_users(project.id)

    assert len(users) == 2
    user_ids = {user["user_id"] for user in users}
    assert project_user.user_id in user_ids
    assert second_user.user_id in user_ids
