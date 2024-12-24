from rest_framework.permissions import BasePermission

from projects.models import ProjectUser
from projects.permissions import get_user_from_jwt
from tasks.models import TaskSubscription


class IsTaskPerformerOrOwner(BasePermission):
    """
    Custom permission to only allow the owner or performer to update the task deadline.
    """

    def has_permission(self, request, view):
        user_id = get_user_from_jwt(request)['user_id']
        task_id = view.kwargs.get('pk')

        print(task_id)

        if request.method in ['GET', 'POST', 'HEAD', 'OPTIONS']:
            return True

        task_subscription = TaskSubscription.objects.filter(
            task_id=task_id,
            user_id=user_id,
            is_subscribed=True
        ).values_list('role', flat=True)

        print(task_subscription)

        if "Owner" in task_subscription or "Performer" in task_subscription:
            return True

        return False

class IsUserOwnerOrEditorOfProject(BasePermission):
    """
    Кастомный пермишен, который проверяет, имеет ли пользователь роль 'owner' или 'editor'
    в проекте, указанном в запросе.
    """

    def has_permission(self, request, view):
        user_id = get_user_from_jwt(request)['user_id']
        project_id = request.data.get('project')

        if not project_id:
            return False

        project_user = ProjectUser.objects.filter(
            project_id=project_id,
            user_id=user_id,
            role__in=['owner', 'editor']
        ).first()

        if project_user:
            return True
        return False