"""Views for listing and creating orders."""

from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Order
from .permissions import IsCustomerUser
from .serializer import OrderCreateSerializer, OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    """Lists the current user's orders (as customer or business) or creates one."""

    def get_queryset(self):
        """Return only orders where the current user is customer or business partner."""
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

    def get_serializer_class(self):
        """Use the create-serializer for POST, the read-serializer for listing."""
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        """Require customer-user permission only for creating, not for listing."""
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Create the order, then return it serialized with the full OrderSerializer."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        output_serializer = OrderSerializer(order)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
