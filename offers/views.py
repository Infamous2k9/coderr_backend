"""Views for listing, creating, and retrieving offers."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response

from .filters import OfferFilter
from .models import Offer, OfferDetail
from .permissions import IsBusinessUser, IsOfferOwner
from .serializer import (
    OfferCreateSerializer,
    OfferDetailSerializer,
    OfferListSerializer,
    OfferRetrieveSerializer,
    OfferUpdateSerializer,
)


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

    def list(self, request, *args, **kwargs):
        """Validate numeric query params before filtering; reject invalid values with 400."""
        for param in ["min_price", "max_delivery_time"]:
            value = request.query_params.get(param)
            if value is not None:
                try:
                    float(value)
                except ValueError:
                    return Response(
                        {param: f"'{value}' is not a valid number."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        """Use the write-serializer for creating, the read-serializer for listing."""
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferListSerializer

    def get_permissions(self):
        """Require business-user permission only for creating, not for listing."""
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates, or deletes a single offer."""

    queryset = Offer.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOfferOwner]

    def get_serializer_class(self):
        """Use the update-serializer for PATCH, the retrieve-serializer otherwise."""
        if self.request.method == "PATCH":
            return OfferUpdateSerializer
        return OfferRetrieveSerializer


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    """Retrieves a single pricing-tier detail (basic/standard/premium) by id."""

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
