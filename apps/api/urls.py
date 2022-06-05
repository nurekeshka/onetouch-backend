from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.accounts.urls')),
    path('games/', include('apps.common.games.urls')),
    path('fields/', include('apps.common.fields.urls'))
]
