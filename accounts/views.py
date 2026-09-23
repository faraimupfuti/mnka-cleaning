from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from accounts.forms import CustomerSignUpForm, CleanerSignUpForm
from accounts.models import User


class MnkaLoginView(LoginView):
    template_name = "accounts/login.html"


def signup_landing(request):
    """Let a visitor choose whether they're booking cleans or offering them."""
    return render(request, "accounts/signup_landing.html")


def customer_signup(request):
    if request.method == "POST":
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("bookings:new")
    else:
        form = CustomerSignUpForm()
    return render(request, "accounts/signup_form.html", {
        "form": form,
        "heading": "Book trusted cleaners",
        "subheading": "Create a customer account to request a clean.",
    })


def cleaner_signup(request):
    if request.method == "POST":
        form = CleanerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("cleaners:onboarding")
    else:
        form = CleanerSignUpForm()
    return render(request, "accounts/signup_form.html", {
        "form": form,
        "heading": "Join as a cleaner",
        "subheading": "Register to receive booking requests in your area.",
    })


@login_required
def dashboard_redirect(request):
    user = request.user
    if user.role == User.Role.CLEANER:
        return redirect("cleaners:dashboard")
    if user.role == User.Role.ADMIN or user.is_staff:
        return redirect("/admin/")
    return redirect("bookings:my_bookings")
