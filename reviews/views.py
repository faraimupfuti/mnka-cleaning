from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from bookings.models import Booking
from reviews.forms import ReviewForm


@login_required
def leave_review(request, booking_pk):
    booking = get_object_or_404(Booking, pk=booking_pk, customer=request.user)
    if booking.status != Booking.Status.COMPLETED:
        messages.error(request, "You can only review a completed booking.")
        return redirect("bookings:my_bookings")
    if hasattr(booking, "review"):
        messages.info(request, "You already reviewed this booking.")
        return redirect("bookings:my_bookings")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            messages.success(request, "Thanks for the feedback!")
            return redirect("bookings:my_bookings")
    else:
        form = ReviewForm()
    return render(request, "reviews/leave_review.html", {"form": form, "booking": booking})
