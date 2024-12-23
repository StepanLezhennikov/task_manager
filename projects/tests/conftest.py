import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from projects.models import Project, ProjectUser



@pytest.fixture
def api_client():
    """Фикстура для API клиента."""
    return APIClient()


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
        user_email="example@gmail.com",
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
    """Данные для создания проекта через API."""
    return {
        "name": "Test Project",
        "description": "Test Description",
        "logo_url": "INvalid URL"
    }

@pytest.fixture
def project_user_data():
    """Данные для создания пользователя в проекте через API."""
    return {
        "user_id": 1,
        "user_email": "example@gmail.com",
        "role": "editor",
    }

@pytest.fixture
def project_user_for_project_data(project):
    """Данные для создания пользователя в проекте через API."""
    return {
        "project": project.pk,
        "role": "editor",
    }

@pytest.fixture
def project_user_for_project_data_invalid(project):
    """Неправильные данные для создания пользователя в проекте через API."""
    return {
        "project": project.pk,
        "role": "invalid role",
    }

@pytest.fixture
def project_user_for_test(project):
    """Фикстура для пользователя, связанного с проектом."""
    return ProjectUser.objects.create(
        project=project,
        user_id=1,
        user_email="example@gmail.com",
        role="reader"
    )


@pytest.fixture
def create_project_user_for_user_id(api_client, project, project_user_data):
    """Фикстура для создания подписки на проект через API."""
    url = reverse('projectuser-create-for-user', kwargs={'user_id': 1})
    response = api_client.post(url, data=project_user_data, format='json')
    return response


@pytest.fixture
def user_projects_url():
    """Фикстура для URL, который возвращает проекты пользователя."""
    return reverse('projectuser-get-user-projects', kwargs={'user_id': 1})


@pytest.fixture
def user_projects_response(api_client, project_user_for_test, user_projects_url):
    """Фикстура для тестирования проектов пользователя."""
    response = api_client.get(user_projects_url)
    return response


@pytest.fixture
def project_list_url():
    """URL для списка проектов."""
    return reverse('project-list')


@pytest.fixture
def project_user_list_url():
    """URL для списка пользователей проекта."""
    return reverse('projectuser-list')


@pytest.fixture
def create_project(api_client, project_data):
    """Фикстура для создания проекта через API."""
    response = api_client.post(reverse('project-list'), data=project_data, format='json')
    return response
