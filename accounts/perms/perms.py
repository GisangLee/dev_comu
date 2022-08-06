from rest_framework.permissions import BasePermission

class LoggedInRequired(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_deleted)

class AllowAny(BasePermission):

    def has_permission(self, request, view):
        return True