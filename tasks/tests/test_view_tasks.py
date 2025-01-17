import pytest
from rest_framework import status

from tasks.models import Task, TaskSubscription
from tasks.tests.conftest import TASKS_URL, TASK_SUBSCRIPTIONS_URL


@pytest.mark.django_db
def test_create_task(api_client, task_data_views):
    """Тест создания задачи через TaskViewSet."""
    response = api_client.post(TASKS_URL, data=task_data_views)
    assert response.status_code == status.HTTP_201_CREATED
    created_task = Task.objects.get(title=task_data_views["title"])
    assert created_task.description == task_data_views["description"]
    assert created_task.status == task_data_views["status"]


@pytest.mark.django_db
def test_create_task_with_invalid_data(api_client, invalid_task_data):
    response = api_client.post(TASKS_URL, data=invalid_task_data)
    print(response.data, response.status_code)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_list_tasks(api_client, task_data_filters):
    """Тест списка задач через TaskViewSet."""
    response = api_client.get(TASKS_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("count") == len(task_data_filters)


@pytest.mark.django_db
def test_update_task_deadline(api_client, task_data_views):
    """Тест обновления срока выполнения задачи через UpdateTaskDeadlineView."""
    task = Task.objects.create(
        title=task_data_views["title"],
        description=task_data_views["description"],
        project_id=task_data_views["project"],
        status=task_data_views["status"],
        deadline=task_data_views["deadline"],
    )
    updated_deadline = {"deadline": "2025-01-01T00:00:00Z"}
    response = api_client.patch(
        f"/tasks/{task.pk}/deadline", data=updated_deadline, format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.deadline.isoformat() == "2025-01-01T00:00:00+00:00"


@pytest.mark.django_db
def test_update_task_deadline_invalid_task(api_client):
    response = api_client.patch(
        "/tasks/999/deadline", data={"deadline": "2025-01-01T00:00:00Z"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_task_subscription(api_client, task_data_views):
    """Тест создания подписки на задачу через TaskSubscriptionViewSet."""
    task = Task.objects.create(
        title=task_data_views["title"],
        description=task_data_views["description"],
        project_id=task_data_views["project"],
        status=task_data_views["status"],
        deadline=task_data_views["deadline"],
    )
    subscription_data = {"user_id": 1, "task": task.pk}
    response = api_client.post(TASK_SUBSCRIPTIONS_URL, data=subscription_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_subscription = TaskSubscription.objects.get(task=task)
    assert created_subscription.user_id == 1


@pytest.mark.django_db
def test_list_task_subscriptions(api_client, task_data_views):
    """Тест списка подписок через TaskSubscriptionViewSet."""
    task = Task.objects.create(
        title=task_data_views["title"],
        description=task_data_views["description"],
        project_id=task_data_views["project"],
        status=task_data_views["status"],
        deadline=task_data_views["deadline"],
    )
    TaskSubscription.objects.create(user_id=1, task=task)

    response = api_client.get(TASK_SUBSCRIPTIONS_URL)
    assert response.status_code == status.HTTP_200_OK

    count_res = response.data.get("count")
    assert count_res == 1
    assert response.data["results"][0]["user_id"] == 1
