from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """Allow access only to object owners (objects with a 'user' attribute)."""
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "user", None) == request.user