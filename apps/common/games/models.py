from django.db.models.signals import post_save
from apps.common.fields.models import Field
from apps.telegram.models import Telegram
from apps.telegram.constants import Emoji
from .constants import PLAYER_POSITIONS
from apps.accounts.models import User
from django.dispatch import receiver
from .constants import TEAM_NAMES
from django.db import models
from datetime import date


class Player(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='user')
    telegram = models.ForeignKey(Telegram, on_delete=models.CASCADE, null=True, blank=True, verbose_name='telegram')
    position = models.CharField(max_length=2, choices=PLAYER_POSITIONS, default='PL')

    class Meta:
        verbose_name = 'игрок'
        verbose_name_plural = 'игроки'
    
    def __str__(self):
        return self.user.get_full_name() if self.user else self.telegram.get_full_name()


class Team(models.Model):
    class Colors(models.TextChoices):
        orange = ('Оранжевые', Emoji.orange.value)
        blue = ('Синие', Emoji.blue.value)
        green = ('Зеленые', Emoji.green.value)

    name = models.CharField(max_length=50, verbose_name='name')
    players = models.ManyToManyField(Player, blank=True, verbose_name='players')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name='game')
    emoji = models.CharField(choices=Colors.choices, max_length=50, verbose_name='emoji')

    class Meta:
        verbose_name = 'команда'
        verbose_name_plural = 'команды'
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
        verbose_name = 'игра'
        verbose_name_plural = 'игры'
        ordering = ('date', 'field')
    
    def __str__(self):
        return f'{self.start.strftime("%H:%M")} - {self.end.strftime("%H:%M")}: {self.form - 1}+1, {self.field.address}'

    def players_left(self):
        teams = Team.objects.filter(game=self)
        available_places = len(teams) * self.form

        for team in teams:
            available_places -= team.players.count()

        return available_places
    
    def is_today(self) -> bool:
        return self.date == date.today()
    
    def detailed(self) -> dict:
        return {
            'адрес': self.field,
            'формат': f'{self.form - 1} + 1',
            'дата': self.date,
            'начало': self.start,
            'конец': self.end 
        }
    
    def teams(self) -> list:
        return Team.objects.filter(game=self)


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

