from django.db import models
from django.urls import reverse


class ServiceCategory(models.Model):
    """Top-level grouping shown on the services page, e.g. Residential, Office."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(
        max_length=50, blank=True,
        help_text="Name of an icon in static/icons/ (without extension), e.g. 'home'",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "service categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Service(models.Model):
    """A bookable service, e.g. 'Deep Cleaning - 2 bedroom'."""

    class PricingUnit(models.TextChoices):
        FLAT = "flat", "Flat rate"
        PER_HOUR = "per_hour", "Per hour"
        PER_ROOM = "per_room", "Per room"

    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name="services")
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=9, decimal_places=2)
    pricing_unit = models.CharField(max_length=10, choices=PricingUnit.choices, default=PricingUnit.FLAT)
    estimated_duration_minutes = models.PositiveIntegerField(default=120)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category__order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("services:detail", args=[self.slug])

    @property
    def price_display(self):
        unit_label = {
            self.PricingUnit.FLAT: "",
            self.PricingUnit.PER_HOUR: "/hour",
            self.PricingUnit.PER_ROOM: "/room",
        }[self.pricing_unit]
        return f"${self.base_price}{unit_label}"
