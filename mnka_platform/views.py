from django.shortcuts import render

from services.models import ServiceCategory


def home(request):
    categories = ServiceCategory.objects.prefetch_related("services")[:6]
    return render(request, "home.html", {"categories": categories})
