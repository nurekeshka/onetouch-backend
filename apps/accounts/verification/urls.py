from django.urls import path
from .constants import VerificationRoutes
from . import views

urlpatterns = [
    path('create/', views.CreatePhoneVerification.as_view(), name=VerificationRoutes.create.value),
    path('verify/', views.ConfirmVerification.as_view(), name=VerificationRoutes.verify.value)
]
