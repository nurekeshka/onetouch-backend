from django.urls import path, include
from . import views

urlpatterns = [
    path('get-all/', views.get_all),
]
