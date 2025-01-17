from datetime import timedelta

import pytest
from rest_framework import status
from django.utils.timezone import now

from tasks.models import Task, TaskSubscription
from tasks.tests.conftest import TASKS_URL, TASK_SUBSCRIPTIONS_URL


@pytest.mark.django_db
def test_create_task(api_client, admin_headers, task_data_views):
    """Тест создания задачи через TaskViewSet."""
    api_client.credentials(HTTP_AUTHORIZATION=admin_headers["Authorization"])
    response = api_client.post(TASKS_URL, data=task_data_views)
    assert response.status_code == status.HTTP_201_CREATED
    created_task = Task.objects.get(title=task_data_views["title"])
    assert created_task.description == task_data_views["description"]
    assert created_task.status == task_data_views["status"]


@pytest.mark.django_db
def test_create_task_with_invalid_data(api_client, admin_headers, invalid_task_data):
    api_client.credentials(HTTP_AUTHORIZATION=admin_headers["Authorization"])
    response = api_client.post(TASKS_URL, data=invalid_task_data)
    print(response.data, response.status_code)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_list_tasks(api_client, admin_headers, task_data_filters):
    """Тест списка задач через TaskViewSet."""
    api_client.credentials(HTTP_AUTHORIZATION=admin_headers["Authorization"])
    response = api_client.get(TASKS_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("count") == len(task_data_filters)


@pytest.mark.django_db
def test_update_task_deadline(api_client, admin_headers, task):
    """Тест обновления срока выполнения задачи через UpdateTaskDeadlineView."""
    api_client.credentials(HTTP_AUTHORIZATION=admin_headers["Authorization"])
    url = f"/tasks/{task.pk}/deadline"
    updated_deadline = {"deadline": now() + timedelta(days=1)}
    response = api_client.patch(url, data=updated_deadline, format="json")
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.deadline == updated_deadline["deadline"]


@pytest.mark.django_db
def test_update_task_deadline_invalid_task(api_client, admin_headers):
    api_client.credentials(HTTP_AUTHORIZATION=admin_headers["Authorization"])
    response = api_client.patch(
        "/tasks/999/deadline", data={"deadline": now() + timedelta(days=1)}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_task_subscription(api_client, admin_headers, task):
    """Тест создания подписки на задачу через TaskSubscriptionViewSet."""
    api_client.credentials(HTTP_AUTHORIZATION=admin_headers["Authorization"])
    subscription_data = {"user_id": 5, "task": task.pk}
    response = api_client.post(TASK_SUBSCRIPTIONS_URL, data=subscription_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_subscription = TaskSubscription.objects.filter(task=task).values_list(
        "user_id", flat=True
    )
    assert subscription_data["user_id"] in created_subscription


@pytest.mark.django_db
def test_list_task_subscriptions(api_client, admin_headers, task):
    """Тест списка подписок через TaskSubscriptionViewSet."""
    api_client.credentials(HTTP_AUTHORIZATION=admin_headers["Authorization"])

    response = api_client.get(TASK_SUBSCRIPTIONS_URL)
    assert response.status_code == status.HTTP_200_OK

    count_res = response.data.get("count")
    assert count_res == 1
    assert response.data["results"][0]["user_id"] == 1
