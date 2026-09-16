"""Serializers for creating and listing orders."""

from rest_framework import serializers

from offers.models import OfferDetail
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Represents an order for both listing and the create-response."""

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class OrderCreateSerializer(serializers.Serializer):
    """Creates an Order by snapshotting the referenced OfferDetail's data."""

    offer_detail_id = serializers.IntegerField()

    def validate_offer_detail_id(self, value):
        """Ensure the referenced OfferDetail actually exists."""
        if not OfferDetail.objects.filter(id=value).exists():
            raise serializers.ValidationError("This offer detail does not exist.")
        return value

    def create(self, validated_data):
        """Copy the OfferDetail's data into a new Order for the current customer."""
        offer_detail = OfferDetail.objects.get(id=validated_data["offer_detail_id"])
        customer_user = self.context["request"].user

        return Order.objects.create(
            customer_user=customer_user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )
