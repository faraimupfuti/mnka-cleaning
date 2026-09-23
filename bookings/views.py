from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from bookings.forms import BookingForm
from bookings.models import Booking


@login_required
def new_booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.price = booking.service.base_price
            booking.save()
            messages.success(request, "Booking request sent! We'll confirm a cleaner shortly.")
            return redirect("bookings:my_bookings")
    else:
        form = BookingForm()
        service_slug = request.GET.get("service")
        if service_slug:
            form.fields["service"].initial = form.fields["service"].queryset.filter(
                slug=service_slug
            ).values_list("pk", flat=True).first()
    return render(request, "bookings/new_booking.html", {"form": form})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, "bookings/my_bookings.html", {"bookings": bookings})


@login_required
def cleaner_update_status(request, pk, new_status):
    booking = get_object_or_404(Booking, pk=pk)
    if not request.user.is_cleaner or booking.cleaner_id != request.user.cleaner_profile.pk:
        messages.error(request, "You can't update that booking.")
        return redirect("cleaners:dashboard")
    try:
        booking.set_status(new_status)
        messages.success(request, f"Booking marked as {booking.get_status_display()}.")
    except ValidationError as exc:
        messages.error(request, str(exc.message))
    return redirect("cleaners:dashboard")
