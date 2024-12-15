from django.urls import path, include
from rest_framework.routers import DefaultRouter

from projects.views import ProjectViewSet, ProjectUserViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'project_users', ProjectUserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]