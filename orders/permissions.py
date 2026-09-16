"""Permission classes for the orders endpoints."""

from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """Allows access only to authenticated users with a customer profile."""

    def has_permission(self, request, view):
        """Return True only if the user is authenticated and their profile type is customer."""
        return (
            request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.type == "customer"
        )


class IsOrderBusinessUser(permissions.BasePermission):
    """Allows status updates only by the business user involved in the order."""

    def has_object_permission(self, request, view, obj):
        """Return True only if the request user is the order's business_user."""
        return obj.business_user == request.user
