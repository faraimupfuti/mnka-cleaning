from django.urls import path

from cleaners import views

app_name = "cleaners"

urlpatterns = [
    path("onboarding/", views.onboarding, name="onboarding"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
