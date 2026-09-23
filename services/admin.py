from django.contrib import admin

from services.models import ServiceCategory, Service


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ServiceInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "base_price", "pricing_unit", "is_active")
    list_filter = ("category", "is_active", "pricing_unit")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
