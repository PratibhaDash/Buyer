from rest_framework import permissions
from .models import UserRoles


class AdminAllOtherReadOnly(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH", "DELETE")

    def has_permission(self, request, view):
        if request.user.is_authenticated or (request.method in permissions.SAFE_METHODS):
            return True

    def has_object_permission(self, request, view, obj):
        user_role = UserRoles.objects.filter(user=request.user).values_list('role', flat=True)
        print(user_role)
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.created_by == request.user:
            return True
        if request.method not in self.edit_methods:
            return True
        return False
