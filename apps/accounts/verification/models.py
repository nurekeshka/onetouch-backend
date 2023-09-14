from ..constants import CONFIRMED
from django.db import models


class PhoneVerification(models.Model):
    phone = models.CharField(max_length=15, unique=True, verbose_name='телефонный номер')
    code = models.CharField(max_length=10, verbose_name='код подтверждения')

    class Meta:
        verbose_name = 'верификация'
        verbose_name_plural = 'верификации'
    
    def confirm(self, code: str):
        if self.code == code:
            self.code = CONFIRMED
            self.save()
            return True
        else:
            return False
