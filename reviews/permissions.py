"""Permission classes for the reviews endpoints."""

from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """Allows creating reviews only to authenticated users with a customer profile."""

    def has_permission(self, request, view):
        """Return True only if the user is authenticated and their profile type is customer."""
        return (
            request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.type == "customer"
        )


class IsReviewOwner(permissions.BasePermission):
    """Allows write access only to the user who wrote the review."""

    def has_object_permission(self, request, view, obj):
        """Return True only if the request user is the review's reviewer."""
        return obj.reviewer == request.user
