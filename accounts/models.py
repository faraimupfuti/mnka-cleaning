from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    A single custom user model shared by customers and cleaners.
    The role decides which profile (CleanerProfile / CustomerProfile)
    the account is paired with and which dashboard it lands on.
    """

    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        CLEANER = "cleaner", "Cleaner"
        ADMIN = "admin", "Admin"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)

    # Shared address fields (a customer's default job address, or a
    # cleaner's base location for distance/area matching).
    address_line = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_cleaner(self):
        return self.role == self.Role.CLEANER

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    notes = models.TextField(blank=True, help_text="Gate codes, pets, access notes, etc.")

    def __str__(self):
        return f"Customer profile: {self.user}"
