import pytest
from rest_framework import status

from tasks.tests.conftest import TASKS_URL


@pytest.mark.django_db
def test_ordering_tasks(api_client, task_data_filters):
    """Тест сортировки задач по названию."""
    response = api_client.get(TASKS_URL, {"ordering": "title"})
    assert response.status_code == status.HTTP_200_OK
    titles = [task["title"] for task in response.data.get('results')]
    assert titles == sorted(titles)