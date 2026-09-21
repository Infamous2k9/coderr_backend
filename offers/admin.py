"""Admin registrations for the offers app."""

from django.contrib import admin

from .models import Offer, OfferDetail


class OfferDetailInline(admin.TabularInline):
    """Shows an offer's details directly inside the Offer admin page."""

    model = OfferDetail
    extra = 0


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """Admin configuration for Offer, with inline OfferDetails."""

    list_display = ("title", "user", "created_at", "updated_at")
    list_filter = ("created_at",)
    inlines = [OfferDetailInline]


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    """Admin configuration for OfferDetail as a standalone list."""

    list_display = ("title", "offer", "offer_type", "price", "delivery_time_in_days")
    list_filter = ("offer_type",)
