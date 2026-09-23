from django.urls import path

from bookings import views

app_name = "bookings"

urlpatterns = [
    path("new/", views.new_booking, name="new"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("<int:pk>/status/<str:new_status>/", views.cleaner_update_status, name="update_status"),
]
