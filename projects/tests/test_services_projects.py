import pytest
from projects.services import ProjectService
from projects.models import ProjectUser, Project


@pytest.mark.django_db
def test_get_user_projects_returns_projects_for_user(project, project_user):
    """Тест получения списка проектов для пользователя."""

    # Вызов сервиса
    projects = ProjectService.get_user_projects(project_user.user_id)
    print(projects)
    # Проверяем, что вернулся список проектов
    assert len(projects) == 1
    assert projects[0]['name'] == project.name
    assert projects[0]['project_users'][0]['user_id'] == project_user.user_id


@pytest.mark.django_db
def test_get_user_projects_empty_for_user():
    """Тест получения пустого списка, если у пользователя нет проектов."""

    # Пользователь без проектов
    user_id = 9999

    # Вызов сервиса
    projects = ProjectService.get_user_projects(user_id)

    # Проверяем, что список пуст
    assert projects == []


@pytest.mark.django_db
def test_get_user_projects_with_multiple_projects(project, project_user_for_test):
    """Тест получения нескольких проектов для пользователя."""

    # Создаем второй проект и привязываем пользователя
    second_project = Project.objects.create(
        name="Second Project",
        description="Second project description"
    )
    ProjectUser.objects.create(
        project=second_project,
        user_id=project_user_for_test.user_id,
        user_email=project_user_for_test.user_email,
        role="editor"
    )

    # Вызов сервиса
    projects = ProjectService.get_user_projects(project_user_for_test.user_id)

    print(projects)
    assert len(projects) == 2
    project_names = {p['name'] for p in projects}
    assert project.name in project_names
    assert second_project.name in project_names


@pytest.mark.django_db
def test_get_user_projects_prefetch_related(project, project_user):
    """Тест, что prefetch_related загружает связанные данные."""

    # Добавляем связанные данные (например, задачи) к проекту
    project.tasks.create(title="Task 1", description="First task")
    project.tasks.create(title="Task 2", description="Second task")

    # Вызов сервиса
    projects = ProjectService.get_user_projects(project_user.user_id)

    # Проверяем, что задачи подгружены
    assert len(projects) == 1
    assert len(projects[0]['tasks']) == 2
    task_titles = {t['title'] for t in projects[0]['tasks']}
    assert "Task 1" in task_titles
    assert "Task 2" in task_titles
