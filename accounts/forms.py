from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True, max_length=20)
    city = forms.CharField(required=False, max_length=100)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone_number", "city"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CUSTOMER
        user.email = self.cleaned_data["email"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.city = self.cleaned_data.get("city", "")
        if commit:
            user.save()
        return user


class CleanerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True, max_length=20)
    city = forms.CharField(required=True, max_length=100, help_text="Suburb / area you serve")
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))
    years_experience = forms.IntegerField(required=False, min_value=0)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone_number", "city"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CLEANER
        user.email = self.cleaned_data["email"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.city = self.cleaned_data.get("city", "")
        if commit:
            user.save()
            profile = user.cleaner_profile
            profile.bio = self.cleaned_data.get("bio", "")
            profile.years_experience = self.cleaned_data.get("years_experience") or 0
            profile.save()
        return user
