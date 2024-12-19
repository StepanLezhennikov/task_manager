import pytest

from tasks.filters import TaskFilter
from tasks.models import Task


@pytest.mark.django_db
def test_task_filter_by_status(task_data_filters):
    filter_data = {'status': 'BACKLOG'}
    filtered_tasks = TaskFilter(data=filter_data, queryset=Task.objects.all()).qs

    assert filtered_tasks.count() == 1
    assert filtered_tasks.first().title == "Write tests"


@pytest.mark.django_db
def test_task_filter_by_name(task_data_filters):
    filter_data = {'title': 'app'}
    filtered_tasks = TaskFilter(data=filter_data, queryset=Task.objects.all()).qs
    assert filtered_tasks.count() == 2