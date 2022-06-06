from django.db import models


class PhoneVerification(models.Model):
    phone = models.CharField(max_length=15, unique=True, verbose_name='phone number')
    code = models.CharField(max_length=10, verbose_name='verification')

    class Meta:
        verbose_name = 'телефонный номер'
        verbose_name_plural = 'телефоные номера'
