from django.shortcuts import get_object_or_404, render

from services.models import Service, ServiceCategory


def service_list(request):
    categories = ServiceCategory.objects.prefetch_related("services").all()
    return render(request, "services/service_list.html", {"categories": categories})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, "services/service_detail.html", {"service": service})
