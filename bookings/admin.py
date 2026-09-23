from django.contrib import admin

from bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "service", "cleaner", "status", "scheduled_for", "price")
    list_filter = ("status", "service__category")
    search_fields = ("customer__username", "customer__email", "address_line", "city")
    autocomplete_fields = ["customer", "cleaner", "service"]
