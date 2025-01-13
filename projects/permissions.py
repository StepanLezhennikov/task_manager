from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsProjectOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.project_users.filter(user_id=request.user_id).exists()
        return obj.project_users.filter(user_id=request.user_id, role="owner").exists()


class IsProjectUserOwnerOrReader(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user_id == obj.user_id
        return obj.user_id == request.user_id and obj.role == "owner"
