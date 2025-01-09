from django.urls import path, include
from rest_framework.routers import DefaultRouter

from projects.views import ProjectViewSet, ProjectUserViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"project_users", ProjectUserViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path(
        "user/<int:user_id>/projects/",
        ProjectUserViewSet.as_view({"post": "add_user_to_project"}),
    ),
    path(
        "project/<int:project_id>/users/",
        ProjectUserViewSet.as_view({"get": "get_project_users"}),
    ),
]
