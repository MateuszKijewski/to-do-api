from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check if user is trying to update their own profile"""

        return obj.id == request.user.id

class TodoListPermission(permissions.BasePermission):
    """Allow user to create and check his Todos"""

    def has_object_permission(self, request, view, obj):
        """Check if user is managing his tasks"""
        return obj.user == request.user

class DeletePermission(permissions.BasePermission):
    """Allow user to delete objects"""

    def has_object_permission(self, request, view, obj):
        """Check if user can delete objects"""
        return obj.user.id == request.user.id