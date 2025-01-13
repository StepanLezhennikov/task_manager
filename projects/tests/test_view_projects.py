import pytest
from rest_framework import status
from projects.models import ProjectUser, Project

PROJECTS_URL = "/api/projects/"
PROJECT_USERS_URL = "/api/project_users/"


@pytest.mark.django_db
def test_create_project(api_client, project_data):
    """Test creating a project using ProjectViewSet."""
    response = api_client.post(PROJECTS_URL, data=project_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_project = Project.objects.get(name=project_data["name"])
    assert created_project.description == project_data["description"]
    assert created_project.logo_url == project_data["logo_url"]


@pytest.mark.django_db
def test_get_project_detail(api_client, project):
    """Test retrieving project details."""
    url = f"{PROJECTS_URL}/{project.pk}/"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == project.name
    assert response.data["description"] == project.description
    assert response.data["logo_url"] == project.logo_url


@pytest.mark.django_db
def test_update_project(api_client, project, project_data):
    """Test updating a project."""
    updated_data = {
        "name": "Updated Project",
        "description": "Updated Description",
        "logo_url": "http://example.com/new-logo.png",
    }
    url = f"{PROJECTS_URL}/{project.pk}/"
    response = api_client.patch(url, data=updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    project.refresh_from_db()
    assert project.name == updated_data["name"]
    assert project.description == updated_data["description"]
    assert project.logo_url == updated_data["logo_url"]


@pytest.mark.django_db
def test_update_project_invalid_data(api_client, project):
    """Test updating a project with invalid data."""
    updated_data = {"name": "", "description": "Updated Description"}
    url = f"{PROJECTS_URL}/{project.pk}/"
    response = api_client.patch(url, data=updated_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_project_user_for_user(api_client, project_user_for_project_data):
    """Test adding a user to a project using ProjectUserViewSet."""
    project_id = project_user_for_project_data["project"]
    user_url = f"/api/project_users/{project_id}/add-user-to-project/"
    response = api_client.post(
        user_url, data=project_user_for_project_data, format="json"
    )
    assert response.status_code == status.HTTP_201_CREATED

    created_user = ProjectUser.objects.get(user_id=1)
    assert created_user.project.pk == project_id
    assert created_user.role == project_user_for_project_data["role"]


@pytest.mark.django_db
def test_create_project_user_with_invalid_data(
    api_client, project_user_for_project_data_invalid
):
    """Test adding a user with invalid data to a project."""
    project_id = project_user_for_project_data_invalid["project"]
    user_url = f"/api/project_users/{project_id}/add-user-to-project/"
    response = api_client.post(
        user_url, data=project_user_for_project_data_invalid, format="json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_user_projects(api_client, project, project_user_for_test):
    """Test retrieving user projects using ProjectUserViewSet."""
    user_url = f"/api/project_users/{project_user_for_test.user_id}/get-user-projects/"
    response = api_client.get(user_url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == project.name
    assert (
        response.data[0]["project_users"][0]["user_email"]
        == project_user_for_test.user_email
    )
