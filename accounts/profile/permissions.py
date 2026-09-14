"""Permission classes for the profile endpoints."""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allows read access to any authenticated user, write access only to the owner."""

    def has_object_permission(self, request, view, obj):
        """Return True for safe methods, or if the request user owns the profile."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
