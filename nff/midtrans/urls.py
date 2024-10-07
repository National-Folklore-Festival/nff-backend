from django.urls import path
from midtrans.views import CreatePaymentAPI, PaymentCallbackAPI

urlpatterns = [
    path('create-payment/', CreatePaymentAPI.as_view()),
    path('payment-notification/', PaymentCallbackAPI.as_view()),
]