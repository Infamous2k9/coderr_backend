"""Serializer for registering (and later logging in) users."""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import Profile


class RegistrationSerializer(serializers.Serializer):
    """Validates registration data and creates a User plus its Profile.

    Not a ModelSerializer, because two objects (User and Profile) are
    created at once and one field (repeated_password) doesn't exist
    on any model.
    """

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=Profile.TYPE_CHOICES)

    def validate_username(self, value):
        """Ensure the username is not already taken."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate(self, data):
        """Check that password and repeated_password match."""
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        """Create the User (with hashed password) and its linked Profile."""
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        Profile.objects.create(user=user, type=validated_data["type"])
        return user


class LoginSerializer(serializers.Serializer):
    """Validates login credentials against Django's authentication backend."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Authenticate the user and attach it to validated_data if successful."""
        user = authenticate(username=data["username"], password=data["password"])
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")
        data["user"] = user
        return data
