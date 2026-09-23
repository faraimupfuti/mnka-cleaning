from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User, CustomerProfile


@receiver(post_save, sender=User)
def create_profile_for_role(sender, instance, created, **kwargs):
    """
    When a user is first created, attach the matching profile.
    Cleaner profiles are created here too (import kept local to avoid
    a circular import between accounts and cleaners at startup).
    """
    if not created:
        return

    if instance.role == User.Role.CUSTOMER:
        CustomerProfile.objects.get_or_create(user=instance)
    elif instance.role == User.Role.CLEANER:
        from cleaners.models import CleanerProfile

        CleanerProfile.objects.get_or_create(user=instance)
