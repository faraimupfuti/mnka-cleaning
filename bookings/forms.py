from django import forms

from bookings.models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["service", "address_line", "city", "scheduled_for", "notes"]
        widgets = {
            "scheduled_for": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["scheduled_for"].input_formats = ["%Y-%m-%dT%H:%M"]
