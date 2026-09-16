"""Data model for reviews left by customers on business profiles."""

from django.contrib.auth.models import User
from django.db import models


class Review(models.Model):
    """A rating and comment left by a customer for a business user."""

    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_reviews"
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="written_reviews"
    )
    rating = models.PositiveSmallIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("business_user", "reviewer")

    def __str__(self):
        """Human-readable representation for the admin interface and shell."""
        return (
            f"{self.reviewer.username} -> {self.business_user.username} ({self.rating})"
        )
