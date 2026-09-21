"""Views for listing and creating orders."""

from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .permissions import IsCustomerUser, IsOrderBusinessUser
from .serializer import OrderCreateSerializer, OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    """Lists the current user's orders (as customer or business) or creates one."""

    pagination_class = None

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


class OrderUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    """Updates an order's status (business user only) or deletes it (staff only)."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        """Require IsAdminUser for delete, IsOrderBusinessUser for status updates."""
        if self.request.method == "DELETE":
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated(), IsOrderBusinessUser()]

    def patch(self, request, *args, **kwargs):
        """Update only the status field, ignoring any other fields in the request."""
        order = self.get_object()
        new_status = request.data.get("status")

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {"status": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)


class OrderCountView(APIView):
    """Returns the number of in-progress orders for a given business user."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id):
        """Count orders with status in_progress for the given business_user_id."""
        get_object_or_404(User, id=business_user_id)
        count = Order.objects.filter(
            business_user_id=business_user_id, status="in_progress"
        ).count()
        return Response({"order_count": count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    """Returns the number of completed orders for a given business user."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id):
        """Count orders with status completed for the given business_user_id."""
        get_object_or_404(User, id=business_user_id)
        count = Order.objects.filter(
            business_user_id=business_user_id, status="completed"
        ).count()
        return Response({"completed_order_count": count}, status=status.HTTP_200_OK)
