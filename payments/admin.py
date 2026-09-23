from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("reference", "booking", "method", "status", "amount", "created_at", "paid_at")
    list_filter = ("status", "method")
    search_fields = ("reference", "booking__customer__username", "booking__customer__email")
    readonly_fields = (
        "reference", "paynow_poll_url", "paynow_redirect_url",
        "paynow_transaction_id", "created_at", "updated_at",
    )
