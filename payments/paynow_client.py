"""
Thin wrapper around the `paynow` package (Paynow Zimbabwe's official
Python SDK). Kept in one place so views don't touch the SDK directly,
and so it's obvious where to swap in a different gateway later.
"""

from django.conf import settings
from django.urls import reverse


def _client(request):
    from paynow import Paynow

    return_url = request.build_absolute_uri(reverse("payments:return"))
    result_url = request.build_absolute_uri(reverse("payments:result"))

    return Paynow(
        settings.PAYNOW_INTEGRATION_ID,
        settings.PAYNOW_INTEGRATION_KEY,
        return_url,
        result_url,
    )


def start_web_payment(request, payment):
    """
    Kick off a card/bank payment. Returns Paynow's hosted checkout URL
    to redirect the customer to, or raises on failure.
    """
    paynow = _client(request)
    item = paynow.create_payment(payment.reference, payment.booking.customer.email)
    item.add(payment.booking.service.name, float(payment.amount))
    response = paynow.send(item)

    if not response.success:
        raise PaynowError(getattr(response, "error", "Paynow rejected the payment request."))

    return response


def start_mobile_payment(request, payment, phone_number, method="ecocash"):
    """
    Kick off an EcoCash payment. Returns Paynow's response, which
    carries on-screen instructions (no redirect - the customer
    approves the USSD prompt on their phone).
    """
    paynow = _client(request)
    item = paynow.create_payment(payment.reference, payment.booking.customer.email)
    item.add(payment.booking.service.name, float(payment.amount))
    response = paynow.send_mobile(item, phone_number, method)

    if not response.success:
        raise PaynowError(getattr(response, "error", "Paynow rejected the payment request."))

    return response


def check_status(request, poll_url):
    paynow = _client(request)
    return paynow.check_transaction_status(poll_url)


class PaynowError(Exception):
    pass
