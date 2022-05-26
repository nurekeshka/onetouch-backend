from . import views
from django.urls import path

urlpatterns = [
    path('verification-sms/', views.verification_sms),
    path('verificate-phone/', views.verificate_phone),
]
