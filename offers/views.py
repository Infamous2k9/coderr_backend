"""Views for listing, creating, and retrieving offers."""

from rest_framework import generics, permissions

from .models import Offer
from .permissions import IsBusinessUser
from .serializer import OfferCreateSerializer


class OfferListCreateView(generics.ListCreateAPIView):
    """Lists all offers (GET) or creates a new one (POST, business users only)."""

    queryset = Offer.objects.all()
    serializer_class = OfferCreateSerializer

    def get_permissions(self):
        """Require business-user permission only for creating, not for listing."""
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.IsAuthenticated()]
