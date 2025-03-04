import pytest
from rest_framework import status

from projects.models import Project, ProjectUser

# URL constants
PROJECTS_URL = "/api/v1/projects/"
PROJECT_USERS_URL = "/api/v1/project_users/"


@pytest.mark.django_db
def test_create_project(api_client, admin_headers, project_data):
    """Test creating a new project."""
    api_client.credentials(HTTP_AUTHORIZATION=admin_headers["Authorization"])
    response = api_client.post(PROJECTS_URL, data=project_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Project.objects.filter(name="Test Project data").exists()


@pytest.mark.django_db
def test_update_project(api_client, admin_headers, updated_data, project):
    """Test updating a project."""
    api_client.credentials(HTTP_AUTHORIZATION=admin_headers["Authorization"])
    url = f"{PROJECTS_URL}{project.id}/"
    response = api_client.patch(url, data=updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    project.refresh_from_db()
    assert project.name == "Updated Project"
    assert project.description == "Updated Description"


@pytest.mark.django_db
def test_get_project_users(api_client, project, admin_headers):
    """Test retrieving users of a project."""
    api_client.credentials(HTTP_AUTHORIZATION=admin_headers["Authorization"])
    url = f"/project/{project.id}/users/"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["user_id"] == 1
    assert response.data[0]["role"] == ProjectUser.RoleChoices.OWNER
