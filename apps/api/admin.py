from django.contrib import admin
from . import models


@admin.register(models.Photo)
class Photo(admin.ModelAdmin):
    list_display = ('id', 'link')
    fields = ('link',)
