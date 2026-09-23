from django import forms

from payments.models import Payment


class PaymentMethodForm(forms.Form):
    method = forms.ChoiceField(choices=Payment.Method.choices, widget=forms.RadioSelect, initial=Payment.Method.WEB)
    phone_number = forms.CharField(
        required=False,
        max_length=20,
        help_text="Required for EcoCash - the number the USSD prompt will be sent to.",
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("method") == Payment.Method.ECOCASH and not cleaned.get("phone_number"):
            self.add_error("phone_number", "Enter the EcoCash number to send the payment request to.")
        return cleaned
