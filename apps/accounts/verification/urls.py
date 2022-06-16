from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_phone_verification, name='start-phone-verification'),
    path('verify/', views.verificate_phone, name='verify-phone')
]
