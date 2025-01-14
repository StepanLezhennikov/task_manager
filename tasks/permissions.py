from rest_framework.permissions import BasePermission

from tasks.models import Task, TaskSubscription
from projects.models import ProjectUser


class IsTaskPerformerOrOwner(BasePermission):
    """
    Custom permission to only allow the owner or performer to update the task deadline.
    """

    def has_permission(self, request, view):
        user_id = request.user_id
        task_id = view.kwargs.get("pk")

        if request.method in ["GET", "POST", "HEAD", "OPTIONS"]:
            return True

        task_subscription = TaskSubscription.objects.filter(
            task_id=task_id, user_id=user_id, is_subscribed=True
        ).values_list("role", flat=True)

        if (
            TaskSubscription.RoleChoices.OWNER in task_subscription
            or TaskSubscription.RoleChoices.PERFORMER in task_subscription
        ):
            return True
        return False


class IsUserOwnerOrEditorOfProject(BasePermission):
    """
    Кастомный пермишен, который проверяет, имеет ли пользователь роль 'owner' или 'editor'
    в проекте.
    """

    def has_permission(self, request, view):
        user_id = request.user_id
        task_id = view.kwargs.get("pk")  # ID задачи (для PUT/DELETE запросов)

        if request.method == "POST":
            project_id = request.data.get("project")
            if not project_id:
                return False

            project_user = ProjectUser.objects.filter(
                project_id=project_id,
                user_id=user_id,
                role__in=[
                    ProjectUser.RoleChoices.OWNER,
                    ProjectUser.RoleChoices.EDITOR,
                ],
            ).exists()

            if project_user:
                return True
            return False

        task = Task.objects.filter(id=task_id).select_related("project").first()
        if not task:
            return False

        project_user = ProjectUser.objects.filter(
            project_id=task.project_id,
            user_id=user_id,
            role__in=[ProjectUser.RoleChoices.OWNER, ProjectUser.RoleChoices.EDITOR],
        ).exists()

        if project_user:
            return True
        return False
