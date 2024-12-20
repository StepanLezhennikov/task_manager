import pytest
from rest_framework import status

from tasks.tests.conftest import TASKS_URL


@pytest.mark.django_db
def test_filter_tasks_by_status(api_client, task_data_filters):
    """Тест фильтрации задач по статусу."""
    response = api_client.get(TASKS_URL, {"status": "BACKLOG"})
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('count') == 1
    first_task = response.data.get('results')[0]
    assert first_task["title"] == "Write tests"

# @pytest.mark.django_db
# def test_task_filter_by_status(task_data_filters):
#     filter_data = {'status': 'BACKLOG'}
#     filtered_tasks = TaskFilter(data=filter_data, queryset=Task.objects.all()).qs
#
#     assert filtered_tasks.count() == 1
#     assert filtered_tasks.first().title == "Write tests"
#
#
# @pytest.mark.django_db
# def test_task_filter_by_name(task_data_filters):
#     filter_data = {'title': 'app'}
#     filtered_tasks = TaskFilter(data=filter_data, queryset=Task.objects.all()).qs
#     assert filtered_tasks.count() == 2