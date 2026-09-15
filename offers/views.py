"""Views for listing, creating, and retrieving offers."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions

from .filters import OfferFilter
from .models import Offer
from .permissions import IsBusinessUser
from .serializer import OfferCreateSerializer, OfferListSerializer


class OfferListCreateView(generics.ListCreateAPIView):
    """Lists all offers (GET, with filtering/search/ordering) or creates one (POST)."""

    queryset = Offer.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = OfferFilter
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]
    ordering = ["-updated_at"]

    def get_serializer_class(self):
        """Use the write-serializer for creating, the read-serializer for listing."""
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferListSerializer

    def get_permissions(self):
        """Require business-user permission only for creating, not for listing."""
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.IsAuthenticated()]
