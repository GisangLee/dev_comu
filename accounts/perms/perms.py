from rest_framework.permissions import BasePermission

class AllowAny(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_deleted)