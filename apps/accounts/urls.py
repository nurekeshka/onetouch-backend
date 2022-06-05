from rest_framework.authtoken import views as drf_token_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('verification/', include('apps.accounts.verification.urls')),
    path('sign-up/', views.create_user),
    path('sign-in/', drf_token_views.obtain_auth_token),
]
