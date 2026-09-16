"""Views for listing, creating, updating, and deleting reviews."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response

from .models import Review
from .permissions import IsCustomerUser, IsReviewOwner
from .serializer import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    """Lists all reviews (with filtering/ordering) or creates one (customers only)."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["business_user", "reviewer"]
    ordering_fields = ["updated_at", "rating"]

    def get_permissions(self):
        """Require customer-user permission only for creating, not for listing."""
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        return [permissions.IsAuthenticated()]


class ReviewUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    """Updates or deletes a review (owner only)."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewOwner]

    def patch(self, request, *args, **kwargs):
        """Allow updating only rating and description, per the API contract."""
        allowed_fields = {"rating", "description"}
        if not set(request.data.keys()).issubset(allowed_fields):
            return Response(
                {"detail": "Only 'rating' and 'description' can be updated."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return self.partial_update(request, *args, **kwargs)
