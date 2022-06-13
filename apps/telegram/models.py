from django.db import models


class Telegram(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False, verbose_name='id')
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name='username')
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='first name')
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='last name')
    age = models.IntegerField(null=True, blank=True, verbose_name='age')
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name='phone')

    class Meta:
        verbose_name = 'телеграм'
        verbose_name_plural = 'телеграм'

    def is_active(self):
        return bool(self.age and self.phone)
    
    def info(self) -> dict:
        return {
            'имя': self.first_name,
            'фамилия': self.last_name,
            'возраст': self.age,
            'телефон': self.phone
        }
    
    def edit(self) -> dict:
        return {
            'имя': 'first_name',
            'фамилию': 'last_name',
            'возраст': 'age',
            'телефон': 'phone'
        }
    
    def get_full_name(self) -> str:
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
    
    def __str__(self) -> str:
        return self.get_full_name()
