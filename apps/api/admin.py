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
    list_display = ('address', 'latitude', 'longitude', 'photo', 'contacts')
    fields = ('address','latitude', 'longitude', 'photo', 'contacts')

@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('field', 'form', 'date', 'start', 'end')
    fields = ('field', 'form', 'date', 'start', 'end', 'teams')
    order_by = ('date',)

@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'game')
    fields = ('name', 'players', 'game')
    order_by = ('name')
