from .constants import GamesRoutes
from django.urls import path
from . import views

urlpatterns = [
    path('get-all/', views.GamesView.as_view(),
         name=GamesRoutes.all_games.value),
]
