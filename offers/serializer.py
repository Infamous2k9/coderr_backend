"""Serializers for creating, listing, and retrieving offers."""

from rest_framework import serializers

from .models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """Represents a single pricing tier (basic/standard/premium) of an Offer."""

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]
        read_only_fields = ["id"]


class OfferCreateSerializer(serializers.ModelSerializer):
    """Creates an Offer together with its 3 required OfferDetails."""

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]
        read_only_fields = ["id"]

    def validate_details(self, value):
        """Ensure exactly 3 details are provided, one per offer_type."""
        if len(value) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly 3 details."
            )

        types_given = {detail["offer_type"] for detail in value}
        required_types = {"basic", "standard", "premium"}
        if types_given != required_types:
            raise serializers.ValidationError(
                "Details must contain exactly one each of: basic, standard, premium."
            )
        return value

    def create(self, validated_data):
        """Create the Offer, then create each nested OfferDetail linked to it."""
        details_data = validated_data.pop("details")
        offer = Offer.objects.create(
            user=self.context["request"].user, **validated_data
        )

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer
