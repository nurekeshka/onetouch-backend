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
    list_display = ('address', 'photo', 'contacts')
    fields = ('address', 'photo', 'contacts')

@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('field', 'form', 'date', 'start', 'end')
    fields = ('field', 'form', 'date', 'start', 'end', 'signed_users')
    order_by = ('date',)
