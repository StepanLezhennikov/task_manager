from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tasks.views import TaskSubscriptionViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'task_subscriptions', TaskSubscriptionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]