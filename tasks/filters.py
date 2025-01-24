import django_filters

from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Task
        fields = ["title", "status"]
