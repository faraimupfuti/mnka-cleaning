from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from bookings.models import Booking
from payments import paynow_client
from payments.forms import PaymentMethodForm
from payments.models import Payment


def _mark_paid(payment):
    if payment.is_paid:
        return
    payment.status = Payment.Status.PAID
    payment.paid_at = timezone.now()
    payment.save(update_fields=["status", "paid_at", "updated_at"])

    booking = payment.booking
    if booking.status == Booking.Status.PENDING:
        try:
            booking.set_status(Booking.Status.CONFIRMED)
        except ValidationError:
            pass


@login_required
def pay_for_booking(request, booking_pk):
    booking = get_object_or_404(Booking, pk=booking_pk, customer=request.user)

    if booking.payments.filter(status=Payment.Status.PAID).exists():
        messages.info(request, "This booking is already paid for.")
        return redirect("bookings:my_bookings")

    if request.method == "POST":
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment = Payment.objects.create(
                booking=booking,
                method=form.cleaned_data["method"],
                amount=booking.price,
                phone_number=form.cleaned_data.get("phone_number", ""),
            )
            try:
                if payment.method == Payment.Method.ECOCASH:
                    response = paynow_client.start_mobile_payment(
                        request, payment, payment.phone_number, "ecocash"
                    )
                    payment.paynow_poll_url = response.poll_url
                    payment.status = Payment.Status.SENT
                    payment.save(update_fields=["paynow_poll_url", "status", "updated_at"])
                    request.session["pending_payment_id"] = payment.pk
                    return render(request, "payments/mobile_instructions.html", {
                        "booking": booking,
                        "payment": payment,
                        "instructions": getattr(response, "instructions", ""),
                    })
                else:
                    response = paynow_client.start_web_payment(request, payment)
                    payment.paynow_poll_url = response.poll_url
                    payment.paynow_redirect_url = response.redirect_url
                    payment.status = Payment.Status.SENT
                    payment.save(update_fields=[
                        "paynow_poll_url", "paynow_redirect_url", "status", "updated_at"
                    ])
                    request.session["pending_payment_id"] = payment.pk
                    return redirect(response.redirect_url)
            except paynow_client.PaynowError as exc:
                payment.status = Payment.Status.FAILED
                payment.save(update_fields=["status", "updated_at"])
                messages.error(request, f"Payment could not be started: {exc}")
    else:
        form = PaymentMethodForm()

    return render(request, "payments/pay.html", {"form": form, "booking": booking})


@login_required
def payment_return(request):
    """Customer lands here after completing (or cancelling) checkout on Paynow's site."""
    payment_id = request.session.get("pending_payment_id")
    payment = Payment.objects.filter(pk=payment_id, booking__customer=request.user).first()

    if payment and payment.paynow_poll_url and not payment.is_paid:
        try:
            status = paynow_client.check_status(request, payment.paynow_poll_url)
            if getattr(status, "paid", False):
                _mark_paid(payment)
        except paynow_client.PaynowError:
            pass

    return render(request, "payments/return.html", {"payment": payment})


@login_required
def check_payment_status(request, payment_pk):
    """Manual 'I've paid, check now' button for the EcoCash instructions page."""
    payment = get_object_or_404(Payment, pk=payment_pk, booking__customer=request.user)
    if not payment.is_paid and payment.paynow_poll_url:
        try:
            status = paynow_client.check_status(request, payment.paynow_poll_url)
            if getattr(status, "paid", False):
                _mark_paid(payment)
                messages.success(request, "Payment confirmed - thank you!")
            else:
                messages.info(request, "Still waiting for payment confirmation from Paynow.")
        except paynow_client.PaynowError as exc:
            messages.error(request, f"Couldn't check payment status: {exc}")
    return redirect("bookings:my_bookings")


@csrf_exempt
@require_POST
def payment_result(request):
    """
    Server-to-server callback Paynow calls with status updates. We
    don't trust the POST body's status field on its own - we look up
    the payment by reference, then re-check status directly against
    Paynow's API using the stored poll url before marking it paid.
    """
    reference = request.POST.get("reference")
    payment = Payment.objects.filter(reference=reference).first()

    if payment and payment.paynow_poll_url and not payment.is_paid:
        try:
            status = paynow_client.check_status(request, payment.paynow_poll_url)
            if getattr(status, "paid", False):
                _mark_paid(payment)
            elif getattr(status, "status", "").lower() in ("cancelled", "failed"):
                payment.status = Payment.Status.FAILED
                payment.save(update_fields=["status", "updated_at"])
        except paynow_client.PaynowError:
            pass

    return HttpResponse("OK")
