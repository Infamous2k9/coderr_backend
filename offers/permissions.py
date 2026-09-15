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


class IsOfferOwner(permissions.BasePermission):
    """Allows write access only to the user who created the offer."""

    def has_object_permission(self, request, view, obj):
        """Return True for safe methods, or if the request user owns the offer."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
