from django import forms

from cleaners.models import CleanerProfile


class CleanerOnboardingForm(forms.ModelForm):
    class Meta:
        model = CleanerProfile
        fields = [
            "bio",
            "years_experience",
            "profile_photo",
            "id_document",
            "services_offered",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
            "services_offered": forms.CheckboxSelectMultiple,
        }
