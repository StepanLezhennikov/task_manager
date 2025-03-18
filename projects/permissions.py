from rest_framework.permissions import SAFE_METHODS, BasePermission

from projects.models import ProjectUser


class HasAccessToProject(BasePermission):
    """
    Permission class to check if the user has access to the specified project.
    """

    def has_object_permission(self, request, view, obj):
        return ProjectUser.objects.filter(
            user_id=request.user_data.id, project_id=request.data.get("project")
        ).exists()


class IsProjectUserReader(BasePermission):
    """
    Permission class to allow read-only access for project users.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            and ProjectUser.objects.filter(user_id=request.user_data.id).exists()
        )


class IsProjectUserOwner(BasePermission):
    """
    Permission class to allow actions only for project owners.
    """

    def has_object_permission(self, request, view, obj):
        return ProjectUser.objects.filter(
            user_id=request.user_data.id, role=ProjectUser.RoleChoices.OWNER
        ).exists()
