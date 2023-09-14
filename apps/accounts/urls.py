from rest_framework.authtoken import views as drf_token_views
from django.urls import path, include
from .constants import AccountsRoutes
from . import views

urlpatterns = [
    path('verification/', include('apps.accounts.verification.urls')),
    path('sign-up/', views.AccountsView.as_view(), name=AccountsRoutes.sign_up.value),
    path('sign-in/', drf_token_views.obtain_auth_token, name=AccountsRoutes.sign_in.value),
]
