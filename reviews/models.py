from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from bookings.models import Booking


class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="review")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}\u2605 for booking #{self.booking_id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._recalculate_cleaner_rating()

    def _recalculate_cleaner_rating(self):
        cleaner = self.booking.cleaner
        if not cleaner:
            return
        agg = Review.objects.filter(booking__cleaner=cleaner).aggregate(models.Avg("rating"))
        cleaner.average_rating = agg["rating__avg"] or 0
        cleaner.save(update_fields=["average_rating"])
