from django.core.management.base import BaseCommand
from django.utils.text import slugify

from services.models import Service, ServiceCategory

CATALOG = [
    ("Residential Cleaning", "home", [
        ("Standard Home Clean", "Homes, apartments and move-in/move-out cleans.", 40, "flat", 120),
    ]),
    ("Office & Commercial Cleaning", "building", [
        ("Office Clean", "Offices, shops and business premises.", 60, "per_hour", 180),
    ]),
    ("Deep Cleaning", "sparkles", [
        ("Deep Clean", "Thorough, detailed top-to-bottom cleaning.", 80, "flat", 240),
    ]),
    ("Window & Glass Cleaning", "window", [
        ("Window & Glass Clean", "Sparkling windows and clear views.", 25, "flat", 90),
    ]),
    ("Post-Construction Cleaning", "gear", [
        ("Post-Construction Clean", "We clean up the dust, you enjoy the results.", 100, "flat", 300),
    ]),
    ("Regular Cleaning", "broom", [
        ("Weekly Cleaning Package", "Daily, weekly or monthly cleaning packages.", 35, "flat", 120),
    ]),
]


class Command(BaseCommand):
    help = "Seed the service catalog with Mnka's standard categories and services."

    def handle(self, *args, **options):
        for order, (cat_name, icon, services) in enumerate(CATALOG):
            category, _ = ServiceCategory.objects.get_or_create(
                name=cat_name,
                defaults={"slug": slugify(cat_name), "icon": icon, "order": order},
            )
            for name, description, price, unit, duration in services:
                Service.objects.get_or_create(
                    slug=slugify(name),
                    defaults={
                        "category": category,
                        "name": name,
                        "description": description,
                        "base_price": price,
                        "pricing_unit": unit,
                        "estimated_duration_minutes": duration,
                    },
                )
        self.stdout.write(self.style.SUCCESS("Service catalog seeded."))
