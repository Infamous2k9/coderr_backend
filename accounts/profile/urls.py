from django.urls import path

from ..profile.views import ProfileDetailView

urlpatterns = [
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
]
