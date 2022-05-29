from django.urls import path, include
from . import views

urlpatterns = [
    path('core/', include('apps.core.urls')),
    path('games/', views.get_all_games),
    path('test/', views.test)
]
