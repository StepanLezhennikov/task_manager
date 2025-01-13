from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tasks.views import TaskViewSet, UpdateTaskDeadlineView, TaskSubscriptionViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"task_subscriptions", TaskSubscriptionViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    path(
        "tasks/<int:pk>/deadline", UpdateTaskDeadlineView.as_view(), name="add_deadline"
    ),
]
