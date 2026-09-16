"""Serializers for creating, listing, and updating reviews."""

from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Represents a review for listing, creating, and updating."""

    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate(self, data):
        """On creation, ensure this reviewer hasn't already reviewed this business_user."""
        if self.instance is None:
            request = self.context["request"]
            business_user = data.get("business_user")
            if Review.objects.filter(
                business_user=business_user, reviewer=request.user
            ).exists():
                raise serializers.ValidationError(
                    "You have already reviewed this business profile."
                )
        return data

    def create(self, validated_data):
        """Create the review with the current user as reviewer."""
        validated_data["reviewer"] = self.context["request"].user
        return super().create(validated_data)
