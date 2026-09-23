from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from bookings.models import Booking
from cleaners.forms import CleanerOnboardingForm
from cleaners.models import CleanerProfile


def cleaner_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_cleaner:
            messages.error(request, "That page is for registered cleaners.")
            return redirect("accounts:login")
        return view_func(request, *args, **kwargs)

    return _wrapped


@login_required
@cleaner_required
def onboarding(request):
    profile = request.user.cleaner_profile
    if request.method == "POST":
        form = CleanerOnboardingForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thanks! Your profile is under review. We'll notify you once you're verified.",
            )
            return redirect("cleaners:dashboard")
    else:
        form = CleanerOnboardingForm(instance=profile)
    return render(request, "cleaners/onboarding.html", {"form": form})


@login_required
@cleaner_required
def dashboard(request):
    profile = request.user.cleaner_profile
    upcoming = Booking.objects.filter(
        cleaner=profile, status__in=[Booking.Status.CONFIRMED, Booking.Status.PENDING]
    ).order_by("scheduled_for")
    history = Booking.objects.filter(cleaner=profile, status=Booking.Status.COMPLETED).order_by(
        "-scheduled_for"
    )[:10]
    return render(
        request,
        "cleaners/dashboard.html",
        {"profile": profile, "upcoming": upcoming, "history": history},
    )
