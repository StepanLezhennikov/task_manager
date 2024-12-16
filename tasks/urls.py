from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tasks.views import TaskSubscriptionViewSet, TaskViewSet, UpdateTaskDeadlineView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'task_subscriptions', TaskSubscriptionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('add_deadline/<int:pk>/', UpdateTaskDeadlineView.as_view(), name='add_deadline'),
]