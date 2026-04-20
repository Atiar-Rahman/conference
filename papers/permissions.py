from rest_framework.permissions import BasePermission

class IsAdminOrReviewer(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        # admin can do everything
        if user.role == 'admin':
            return True

        # reviewer limited access
        if user.role == 'reviewer':
            # only allow specific actions
            if view.action in ['paper_status_update']:
                return True

        return False
