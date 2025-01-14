from rest_framework.permissions import SAFE_METHODS, BasePermission

from projects.models import ProjectUser


class HasAccessToProject(BasePermission):
    """
    Permission class to check if the user has access to the specified project.
    """

    def has_object_permission(self, request, view, obj):
        print("HasAccessToProject запущен")
        return ProjectUser.objects.filter(
            user_id=request.user_id, project_id=request.data.get("project")
        ).exists()


class IsProjectUserReader(BasePermission):
    """
    Permission class to allow read-only access for project users.
    """

    def has_object_permission(self, request, view, obj):
        print("IsProjectUserReader запущен")
        return (
            request.method in SAFE_METHODS
            and obj.project_users.filter(user_id=request.user_id).exists()
        )


class IsProjectUserOwner(BasePermission):
    """
    Permission class to allow actions only for project owners.
    """

    def has_object_permission(self, request, view, obj):
        print("IsProjectUserOwner запущен")
        return obj.project_users.filter(user_id=request.user_id, role="owner").exists()
