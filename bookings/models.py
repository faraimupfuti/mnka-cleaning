from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from cleaners.models import CleanerProfile
from services.models import Service


class Booking(models.Model):
    """
    A customer's request for a clean. Status moves forward through a
    small state machine — see ALLOWED_TRANSITIONS below.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    ALLOWED_TRANSITIONS = {
        Status.PENDING: {Status.CONFIRMED, Status.CANCELLED},
        Status.CONFIRMED: {Status.IN_PROGRESS, Status.CANCELLED},
        Status.IN_PROGRESS: {Status.COMPLETED, Status.CANCELLED},
        Status.COMPLETED: set(),
        Status.CANCELLED: set(),
    }

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    cleaner = models.ForeignKey(
        CleanerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="jobs"
    )
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="bookings")

    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    notes = models.TextField(blank=True, help_text="Access instructions, special requests, etc.")

    scheduled_for = models.DateTimeField()
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)

    price = models.DecimalField(max_digits=9, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-scheduled_for"]

    def __str__(self):
        return f"Booking #{self.pk} - {self.service.name} for {self.customer}"

    def set_status(self, new_status):
        """Validated status transition - raises if the move isn't allowed."""
        current = self.Status(self.status)
        if new_status not in self.ALLOWED_TRANSITIONS[current]:
            raise ValidationError(
                f"Cannot move booking from '{current.label}' to '{self.Status(new_status).label}'."
            )
        self.status = new_status
        self.save(update_fields=["status", "updated_at"])

    @property
    def is_paid(self):
        return self.payments.filter(status="paid").exists()
