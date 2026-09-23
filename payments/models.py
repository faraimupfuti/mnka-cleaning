import uuid

from django.conf import settings
from django.db import models

from bookings.models import Booking


class Payment(models.Model):
    """
    One payment attempt for a booking, made through Paynow (Zimbabwe's
    card + mobile money gateway). A booking can have more than one
    Payment row if a first attempt fails and the customer retries.
    """

    class Method(models.TextChoices):
        WEB = "web", "Card / bank (Paynow checkout)"
        ECOCASH = "ecocash", "EcoCash"

    class Status(models.TextChoices):
        CREATED = "created", "Created"
        SENT = "sent", "Awaiting payment"
        PAID = "paid", "Paid"
        CANCELLED = "cancelled", "Cancelled"
        FAILED = "failed", "Failed"

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")
    reference = models.CharField(max_length=64, unique=True, default=uuid.uuid4, editable=False)
    method = models.CharField(max_length=10, choices=Method.choices, default=Method.WEB)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.CREATED)

    amount = models.DecimalField(max_digits=9, decimal_places=2)
    phone_number = models.CharField(max_length=20, blank=True, help_text="Used for EcoCash payments")

    paynow_poll_url = models.URLField(blank=True)
    paynow_redirect_url = models.URLField(blank=True)
    paynow_transaction_id = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment {self.reference} - {self.get_status_display()} (${self.amount})"

    @property
    def is_paid(self):
        return self.status == self.Status.PAID
