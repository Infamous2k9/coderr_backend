"""Project-wide aggregating views that don't belong to a single app."""

from django.db.models import Avg
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.models import Profile
from offers.models import Offer
from reviews.models import Review


@api_view(["GET"])
def base_info(request):
    """Return platform-wide statistics: review count, average rating, business count, offer count."""
    review_count = Review.objects.count()
    average_rating = Review.objects.aggregate(avg=Avg("rating"))["avg"] or 0
    business_profile_count = Profile.objects.filter(type="business").count()
    offer_count = Offer.objects.count()

    data = {
        "review_count": review_count,
        "average_rating": round(average_rating, 1),
        "business_profile_count": business_profile_count,
        "offer_count": offer_count,
    }
    return Response(data)
