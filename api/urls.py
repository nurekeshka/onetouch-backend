from django.urls import path
from . import views

urlpatterns = [
    path('profiles/send-sms-verification', views.send_profile_verification, name='send-sms-verification'),
    path('profiles/verify-phone', views.verify_profile_phone, name='verify-phone-number'),
    path('profiles/verified', views.profile_is_verified, name='verified'),
    path('users/create', views.create_verified_user, name='create-verified-user'),
    path('users/sign-in', views.sign_in, name='sign-in'),
    path('users/sign-out', views.sign_out, name='sign-out')
]
