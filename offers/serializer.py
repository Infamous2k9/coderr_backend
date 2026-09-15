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


class UserDetailsSerializer(serializers.Serializer):
    """Minimal representation of the offer's creator, embedded in offer lists."""

    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    username = serializers.CharField(source="user.username")


class OfferDetailLinkSerializer(serializers.Serializer):
    """Represents a single detail as {id, url} instead of the full object."""

    id = serializers.IntegerField()
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        """Build the relative URL pointing to this detail's own endpoint."""
        return f"/offerdetails/{obj.id}/"


class OfferListSerializer(serializers.ModelSerializer):
    """Represents an Offer in the list view, with aggregated price/delivery info."""

    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserDetailsSerializer(source="*", read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_min_price(self, obj):
        """Return the lowest price among this offer's details."""
        return min(detail.price for detail in obj.details.all())

    def get_min_delivery_time(self, obj):
        """Return the shortest delivery time among this offer's details."""
        return min(detail.delivery_time_in_days for detail in obj.details.all())


class OfferDetailUpdateSerializer(serializers.ModelSerializer):
    """Represents a detail update, identified by offer_type instead of id."""

    class Meta:
        model = OfferDetail
        fields = [
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferUpdateSerializer(serializers.ModelSerializer):
    """Updates an Offer and, optionally, one or more of its details by offer_type."""

    details = OfferDetailUpdateSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        """Update simple Offer fields directly, and matching details by offer_type."""
        details_data = validated_data.pop("details", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for detail_data in details_data:
            offer_type = detail_data.pop("offer_type")
            OfferDetail.objects.filter(offer=instance, offer_type=offer_type).update(
                **detail_data
            )

        return instance


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """Represents a single Offer with detail links and aggregated price/delivery info."""

    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
        ]

    def get_min_price(self, obj):
        """Return the lowest price among this offer's details."""
        return min(detail.price for detail in obj.details.all())

    def get_min_delivery_time(self, obj):
        """Return the shortest delivery time among this offer's details."""
        return min(detail.delivery_time_in_days for detail in obj.details.all())
