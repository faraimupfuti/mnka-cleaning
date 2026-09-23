from django.contrib import admin

from cleaners.models import CleanerProfile, ServiceArea, AvailabilitySlot


class ServiceAreaInline(admin.TabularInline):
    model = ServiceArea
    extra = 1


class AvailabilityInline(admin.TabularInline):
    model = AvailabilitySlot
    extra = 1


@admin.register(CleanerProfile)
class CleanerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user", "verification_status", "is_accepting_bookings",
        "average_rating", "completed_jobs",
    )
    list_filter = ("verification_status", "is_accepting_bookings")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
    filter_horizontal = ("services_offered",)
    inlines = [ServiceAreaInline, AvailabilityInline]
    actions = ["mark_verified", "mark_rejected"]

    @admin.action(description="Mark selected cleaners as verified")
    def mark_verified(self, request, queryset):
        queryset.update(verification_status=CleanerProfile.VerificationStatus.VERIFIED)

    @admin.action(description="Mark selected cleaners as rejected")
    def mark_rejected(self, request, queryset):
        queryset.update(verification_status=CleanerProfile.VerificationStatus.REJECTED)
