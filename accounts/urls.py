from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.MnkaLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", views.signup_landing, name="signup_landing"),
    path("signup/customer/", views.customer_signup, name="customer_signup"),
    path("signup/cleaner/", views.cleaner_signup, name="cleaner_signup"),
    path("dashboard/", views.dashboard_redirect, name="dashboard_redirect"),
]
