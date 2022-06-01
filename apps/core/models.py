from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from datetime import date


class Verification(models.Model):
    phone = models.CharField(max_length=15, unique=True, verbose_name='phone number')
    code = models.CharField(max_length=10, verbose_name='verification')


class User(AbstractUser):
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ('username',)

    username = models.CharField(max_length=50, verbose_name='username')
    phone = models.CharField(max_length=15, unique=True, verbose_name='phone number')
    photo = models.URLField(null=True, blank=True, verbose_name='photo link')
    birth_date = models.DateField(null=True, blank=True, verbose_name='birth date')
    email = models.EmailField(null=True, blank=True, verbose_name='email')

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('phone',)
    
    def __str__(self):
        return self.get_full_name()

    def age(self):
        today = date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return age

@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_token(sender, instance, **kwargs):
    Token.objects.get(user=instance).save()
