from django.conf import settings
from django.db import models

from services.models import Service


def _private_storage():
    """Cleaner ID docs go to the private (signed-URL) bucket when S3 is on."""
    if getattr(settings, "USE_S3", False):
        from mnka_platform.storage_backends import PrivateMediaStorage

        return PrivateMediaStorage()
    from django.core.files.storage import default_storage

    return default_storage


def _public_storage():
    if getattr(settings, "USE_S3", False):
        from mnka_platform.storage_backends import PublicMediaStorage

        return PublicMediaStorage()
    from django.core.files.storage import default_storage

    return default_storage


class CleanerProfile(models.Model):
    """Extra info + verification state for a user with role=cleaner."""

    class VerificationStatus(models.TextChoices):
        PENDING = "pending", "Pending review"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cleaner_profile"
    )
    bio = models.TextField(blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    id_document = models.FileField(
        upload_to="cleaner_ids/", blank=True, null=True, storage=_private_storage,
        help_text="National ID or passport - kept private, used only for verification.",
    )
    profile_photo = models.ImageField(upload_to="cleaner_photos/", blank=True, null=True, storage=_public_storage)
    verification_status = models.CharField(
        max_length=10, choices=VerificationStatus.choices, default=VerificationStatus.PENDING
    )
    services_offered = models.ManyToManyField(Service, blank=True, related_name="cleaners")
    is_accepting_bookings = models.BooleanField(default=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    completed_jobs = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_verification_status_display()})"

    @property
    def is_verified(self):
        return self.verification_status == self.VerificationStatus.VERIFIED

    @property
    def can_take_bookings(self):
        return self.is_verified and self.is_accepting_bookings


class ServiceArea(models.Model):
    """Suburb/area a cleaner is willing to travel to."""

    cleaner = models.ForeignKey(CleanerProfile, on_delete=models.CASCADE, related_name="areas")
    area_name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("cleaner", "area_name")

    def __str__(self):
        return self.area_name


class AvailabilitySlot(models.Model):
    """A recurring weekly slot a cleaner is free, used for booking matching."""

    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

    cleaner = models.ForeignKey(CleanerProfile, on_delete=models.CASCADE, related_name="availability")
    weekday = models.IntegerField(choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["weekday", "start_time"]

    def __str__(self):
        return f"{self.get_weekday_display()} {self.start_time}-{self.end_time}"
