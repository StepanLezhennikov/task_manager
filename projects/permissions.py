from rest_framework.permissions import BasePermission, SAFE_METHODS

from projects.models import ProjectUser


#  later change it
def get_user_from_jwt(request):
    return {'user_id': 1, 'email': 'stepanlezennikov@gmail.com'}


class IsProjectOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.project_users.filter(user_id=get_user_from_jwt(request)['user_id']).exists()
        return obj.project_users.filter(user_id=get_user_from_jwt(request)['user_id'], role='owner').exists()

class IsProjectUserOwnerOrReader(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return get_user_from_jwt(request)['user_id'] == obj.user_id
        return obj.user_id == get_user_from_jwt(request)['user_id'] and obj.role == 'owner'
