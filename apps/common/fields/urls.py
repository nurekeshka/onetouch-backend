from django.urls import path
from . import views

urlpatterns = [
    path('create-fake/', views.create_fake_information),
    path('latitude-and-longitude/', views.get_latitude_and_longitude)
]
