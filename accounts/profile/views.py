"""Views for retrieving and updating a user's profile."""

from rest_framework import generics, permissions

from ..models import Profile
from .permissions import IsOwnerOrReadOnly
from .serializer import (
    ProfileSerializer,
    BusinessProfileListSerializer,
    CustomerProfileListSerializer,
)


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """Retrieves (GET) or updates (PATCH) a single profile by user id."""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "user__pk"
    lookup_url_kwarg = "pk"


class BusinessProfileListView(generics.ListAPIView):
    """Lists all business profiles on the platform."""

    queryset = Profile.objects.filter(type="business")
    serializer_class = BusinessProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


class CustomerProfileListView(generics.ListAPIView):
    """Lists all customer profiles on the platform."""

    queryset = Profile.objects.filter(type="customer")
    serializer_class = CustomerProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
