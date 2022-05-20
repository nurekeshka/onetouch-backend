from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(null=False, blank=False, max_length=254)
    photo = models.URLField(max_length=254, null=True, blank=True)
    verification = models.CharField(max_length=6)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
    def __str__(self):
        return self.phone
