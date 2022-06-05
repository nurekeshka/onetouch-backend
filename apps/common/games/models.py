from django.db.models.signals import post_save
from apps.common.fields.models import Field
from apps.accounts.models import User
from django.dispatch import receiver
from .constants import TEAM_NAMES
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=50, verbose_name='name')
    players = models.ManyToManyField(User, blank=True, verbose_name='players')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name='game')

    class Meta:
        verbose_name = 'team'
        verbose_name_plural = 'teams'
        ordering = ('game',)
    
    def __str__(self):
        return self.name


class Game(models.Model):
    field = models.ForeignKey(Field, on_delete=models.PROTECT, verbose_name='field')
    form = models.IntegerField(verbose_name='form')
    date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='date')
    start = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='start')
    end = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='end')

    class Meta:
        verbose_name = 'game'
        verbose_name_plural = 'games'
        ordering = ('date', 'field')
    
    def __str__(self):
        return f'{self.field.address} : {self.form - 1}+1, {self.date}, {self.start} - {self.end}'

    def players_left(self):
        teams = Team.objects.filter(game=self)
        available_places = len(teams) * self.form

        for team in teams:
            available_places -= team.players.count()

        return available_places

@receiver(post_save, sender=Game)
def create_teams(sender, instance, created, **kwargs):
    if created:
        for name in TEAM_NAMES:
            Team.objects.create(
                name=name,
                game=instance
            )

@receiver(post_save, sender=Game)
def save_teams(sender, instance, **kwargs):
    for name in TEAM_NAMES:
        Team.objects.get(
            game=instance,
            name=name
        ).save()

