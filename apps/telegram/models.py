from django.db import models


class Telegram(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False, verbose_name='id')
    username = models.CharField(max_length=50, null=True, blank=True, verbose_name='username')
    first_name = models.CharField(max_length=124, null=True, blank=True, verbose_name='first name')
    last_name = models.CharField(max_length=124, null=True, blank=True, verbose_name='last name')
    age = models.IntegerField(null=True, blank=True, verbose_name='age')
    phone = models.CharField(max_length=70, null=True, blank=True, verbose_name='phone')

    class Meta:
        verbose_name = 'телеграм'
        verbose_name_plural = 'телеграм'

    def is_active(self):
        return bool(self.age and self.phone)
    
    def info(self):
        return {
            'username': self.username, 
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'phone': self.phone
        }
