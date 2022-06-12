from django.contrib import admin
from . import models


@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('field', 'form', 'date', 'start', 'end')
    fields = ('field', 'form', 'date', 'start', 'end')
    order_by = ('date',)

@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'game', 'emoji')
    fields = ('name', 'players', 'game', 'emoji')
    order_by = ('name')

@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram', 'position')
    fields = ('user', 'telegram', 'position')
