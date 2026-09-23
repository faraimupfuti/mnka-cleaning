from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User, CustomerProfile


@admin.register(User)
class MnkaUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "phone_number", "city", "is_staff")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    fieldsets = UserAdmin.fieldsets + (
        ("Mnka profile", {"fields": ("role", "phone_number", "address_line", "city")}),
    )


admin.site.register(CustomerProfile)
