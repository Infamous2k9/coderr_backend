"""Data models for offers and their pricing-tier details."""

from django.contrib.auth.models import User
from django.db import models


class Offer(models.Model):
    """A service offer created by a business user, containing 3 OfferDetails."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="offer_images/", blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Human-readable representation for the admin interface and shell."""
        return self.title


class OfferDetail(models.Model):
    """A single pricing tier (basic/standard/premium) belonging to an Offer."""

    OFFER_TYPE_CHOICES = [
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    ]

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPE_CHOICES)

    def __str__(self):
        """Human-readable representation for the admin interface and shell."""
        return f"{self.offer.title} - {self.offer_type}"
