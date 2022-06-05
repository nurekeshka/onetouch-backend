from rest_framework.authtoken import views as drf_token_views
from . import views
from django.urls import path

urlpatterns = [
    path('verification-sms/', views.verification_sms),
    path('verificate-phone/', views.verificate_phone),
    path('sign-up/', views.create_user),
    path('token/', drf_token_views.obtain_auth_token),
]
