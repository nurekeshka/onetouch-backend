from .constants import FieldsRoutes
from django.urls import path
from . import views

urlpatterns = [
    path('latitude-and-longitude/', views.GeocodeApiView.as_view(),
         name=FieldsRoutes.latitude_longitude.value),
    path('photos/', views.PhotoView.as_view(), name=FieldsRoutes.photos.value),
    path('', views.FieldView.as_view(), name=FieldsRoutes.get_field_by_id.value),
]
