from rest_framework.permissions import BasePermission

from tasks.models import TaskSubscription


class TaskRolesGetMixin:
    @staticmethod
    def get_task_roles(user_id, task_id):
        roles = TaskSubscription.objects.filter(
            task_id=task_id, user_id=user_id, is_subscribed=True
        ).values_list("role", flat=True)
        return roles


class IsSafeMethodPermission(BasePermission):
    """
    Base permission that allows access for safe HTTP methods.
    """

    def has_permission(self, request, view):
        if request.method in ["GET", "POST", "HEAD", "OPTIONS"]:
            return True
        return False


class IsTaskOwner(BasePermission, TaskRolesGetMixin):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        user_id = request.user_id
        task_id = view.kwargs.get("pk")

        roles = self.get_task_roles(user_id, task_id)

        if TaskSubscription.RoleChoices.OWNER in roles:
            return True
        return False


class IsTaskPerformer(BasePermission, TaskRolesGetMixin):
    """
    Custom permission to only allow performers of an object to edit it.
    """

    def has_permission(self, request, view):
        user_id = request.user_id
        task_id = view.kwargs.get("pk")

        roles = self.get_task_roles(user_id, task_id)

        if TaskSubscription.RoleChoices.PERFORMER in roles:
            return True
        return False
