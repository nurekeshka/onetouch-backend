from django.urls import path, include
from . import views

urlpatterns = [
    path('auth/', include('apps.accounts.urls')),
    path('games/', include('apps.common.games.urls')),
    path('test/', views.test),
    path('fake-information/', views.create_fake_info),
]
