"""Data models for the accounts app."""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Extends the Django User with platform-specific additional data.

    Has a 1:1 relationship with User. Is created automatically together
    with the User during registration (see RegistrationSerializer).
    """

    TYPE_CHOICES = [
        ("customer", "Customer"),
        ("business", "Business"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    file = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=50, blank=True, default="")
    description = models.CharField(max_length=500, blank=True, default="")
    working_hours = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Human-readable representation for the admin interface and shell."""
        return f"{self.user.username} ({self.type})"
