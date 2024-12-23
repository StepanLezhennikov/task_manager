import pytest
from rest_framework import status

from projects.models import ProjectUser, Project

PROJECTS_URL = "/api/projects/"
PROJECT_USERS_URL = "/api/project_users/"

@pytest.mark.django_db
def test_create_project(api_client, project_data):
    """Тест создания проекта через ProjectViewSet."""
    response = api_client.post(PROJECTS_URL, data=project_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_project = Project.objects.get(name=project_data["name"])
    assert created_project.description == project_data["description"]
    assert created_project.logo_url == project_data["logo_url"]


@pytest.mark.django_db
def test_create_project_with_invalid_data(api_client, invalid_project_data):
    """Тест создания проекта с некорректными данными."""
    response = api_client.post(PROJECTS_URL, data=invalid_project_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_list_projects(api_client, project_data):
    """Тест списка проектов через ProjectViewSet."""
    response = api_client.get(PROJECTS_URL)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == Project.objects.count()


@pytest.mark.django_db
def test_get_project_detail(api_client, project):
    """Тест получения деталей проекта."""
    response = api_client.get(f"/api/projects/{project.pk}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == project.name
    assert response.data['description'] == project.description
    assert response.data['logo_url'] == project.logo_url


@pytest.mark.django_db
def test_update_project(api_client, project, project_data):
    """Тест обновления проекта."""
    updated_data = {"name": "Updated Project", "description": "Updated Description", "logo_url": "http://example.com/new-logo.png"}
    response = api_client.patch(f"/api/projects/{project.pk}/", data=updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    project.refresh_from_db()
    assert project.name == updated_data["name"]
    assert project.description == updated_data["description"]
    assert project.logo_url == updated_data["logo_url"]


@pytest.mark.django_db
def test_update_project_invalid_data(api_client, project):
    """Тест обновления проекта с некорректными данными."""
    updated_data = {"name": "", "description": "Updated Description", "logo_url": "http://example.com/new-logo.png"}
    response = api_client.patch(f"/api/projects/{project.pk}/", data=updated_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_project_user_for_user(api_client,  project_user_for_project_data):
    """Тест добавления пользователя в проект через ProjectUserViewSet."""
    url = f"/user/1/projects/"
    project_pk  = project_user_for_project_data["project"]
    response = api_client.post(url, data=project_user_for_project_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    created_user = ProjectUser.objects.get(user_id=1)
    assert created_user.project.pk == project_pk
    assert created_user.role == project_user_for_project_data["role"]


@pytest.mark.django_db
def test_create_project_user_with_invalid_data(api_client, project_user_for_project_data_invalid):
    """Тест создания пользователя в проекте с некорректными данными."""
    url = f"/user/1/projects/"
    response = api_client.post(url, data=project_user_for_project_data_invalid)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_list_project_users(api_client, project, project_user_for_test):
    """Тест списка пользователей проекта через ProjectUserViewSet."""
    response = api_client.get(PROJECT_USERS_URL)
    assert response.status_code == status.HTTP_200_OK
    res_count = response.data.get('count')
    assert res_count == 1
    assert response.data.get('results')[0]["role"] == project_user_for_test.role


@pytest.mark.django_db
def test_get_user_projects(api_client, project, project_user_for_test):
    """Тест получения проектов пользователя через ProjectUserViewSet."""
    url = f"/user/{project_user_for_test.user_id}/projects/"
    response = api_client.get(url)
    print(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == project.name
    assert response.data[0]['project_users'][0]['user_email'] == project_user_for_test.user_email
