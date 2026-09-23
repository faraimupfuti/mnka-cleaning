from django.urls import path

from reviews import views

app_name = "reviews"

urlpatterns = [
    path("<int:booking_pk>/new/", views.leave_review, name="new"),
]
