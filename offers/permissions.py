"""Permission classes for the offers endpoints."""

from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """Allows access only to authenticated users with a business profile."""

    def has_permission(self, request, view):
        """Return True only if the user is authenticated and their profile type is business."""
        return (
            request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.type == "business"
        )
