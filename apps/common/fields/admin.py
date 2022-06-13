from django.contrib import admin
from . import models


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'link')
    fields = ('link',)

@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('raiting', 'description', 'user', 'field')

@admin.register(models.Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('address', 'latitude', 'longitude', 'contacts')
    fields = ('address','latitude', 'longitude', 'photo', 'contacts', 'facilities', 'gis_link')

@admin.register(models.Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icons_link')
    fields = ('name', 'icons_link')
    order_by = ('name')
