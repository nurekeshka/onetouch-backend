from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver


class Phone(models.Model):
    phone = models.CharField(max_length=15, unique=True, verbose_name='phone number')
    verification = models.CharField(max_length=10, verbose_name='verification')


class User(AbstractUser):
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('username',)

    username = models.CharField(max_length=50, verbose_name='username')
    phone = models.CharField(max_length=15, unique=True, verbose_name='phone number')
    photo = models.URLField(null=True, blank=True, verbose_name='photo link')
    birth_date = models.DateField(null=True, blank=True, verbose_name='birth date')

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    def __str__(self):
        return self.username

@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_token(sender, instance, **kwargs):
    Token.objects.get(user=instance).save()
