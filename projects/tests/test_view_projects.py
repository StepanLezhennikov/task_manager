import pytest
from rest_framework import status

from projects.models import Project, ProjectUser

# URL constants
PROJECTS_URL = "/api/v1/projects/"
PROJECT_USERS_URL = "/api/v1/project_users/"


@pytest.mark.django_db
def test_update_project(api_client, project, user_data):
    """Test updating a project."""
    api_client.handler._force_user = user_data
    updated_data = {
        "name": "Updated Project",
        "description": "Updated Description",
        "logo_url": "http://example.com/updated-logo.png",
    }
    url = f"{PROJECTS_URL}{project.id}/"
    response = api_client.patch(url, data=updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    project.refresh_from_db()
    assert project.name == "Updated Project"
    assert project.description == "Updated Description"


@pytest.mark.django_db
def test_get_project_users(api_client, project, project_user, user_data):
    """Test retrieving users of a project."""
    api_client.handler._force_user = user_data
    url = f"{PROJECT_USERS_URL}{project.id}/users/"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == project_user.user_id
    assert response.data[0]["role"] == project_user.role


@pytest.mark.django_db
def test_create_project(api_client, user_data):
    """Test creating a new project."""
    api_client.handler._force_user = user_data
    data = {
        "name": "New Project",
        "description": "New Project Description",
        "logo_url": "http://example.com/logo.png",
    }
    response = api_client.post(PROJECTS_URL, data=data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Project.objects.filter(name="New Project").exists()


@pytest.mark.django_db
def test_add_user_to_project(api_client, project, user_data):
    """Test adding a user to a project."""
    api_client.handler._force_user = user_data
    user_data = {"user_id": 2, "role": "viewer"}
    url = f"{PROJECT_USERS_URL}{project.id}/users/"
    response = api_client.post(url, data=user_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert ProjectUser.objects.filter(
        project=project, user_id=2, role="viewer"
    ).exists()
