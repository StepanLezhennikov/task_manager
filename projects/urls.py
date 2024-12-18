from django.urls import path, include
from rest_framework.routers import DefaultRouter

from projects.views import ProjectViewSet, ProjectUserViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'project_users', ProjectUserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('user/<int:user_id>/projects/', ProjectUserViewSet.as_view({'get': 'get_user_projects', 'post': 'create_for_user'})),
]
