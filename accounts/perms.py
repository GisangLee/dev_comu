from rest_framework.permissions import BasePermission

class LoggedInRequired(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            if request.user.is_deleted:
                return False
            else:

                return True
        else:
            return False


class AllowAny(BasePermission):

    def has_permission(self, request, view):
        return True


class AdminOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        else:
            if request.user.is_admin:
                return True
                
            else:
                return False