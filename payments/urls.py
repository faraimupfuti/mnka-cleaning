from django.urls import path

from payments import views

app_name = "payments"

urlpatterns = [
    path("pay/<int:booking_pk>/", views.pay_for_booking, name="pay"),
    path("return/", views.payment_return, name="return"),
    path("result/", views.payment_result, name="result"),
    path("status/<int:payment_pk>/", views.check_payment_status, name="status"),
]
