from django import forms

from reviews.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.RadioSelect(choices=[(i, f"{i} star{'s' if i != 1 else ''}") for i in range(5, 0, -1)]),
            "comment": forms.Textarea(attrs={"rows": 3}),
        }
