from apps.accounts.models import User
from django.db import models


class Photo(models.Model):
    link = models.URLField(null=True, blank=True, unique=True, verbose_name='link')

    class Meta:
        verbose_name = 'фото'
        verbose_name_plural = 'фото'
        ordering = ('link',)

    def __str__(self):
        return self.link


class Feedback(models.Model):
    raiting = models.FloatField(verbose_name='raiting')
    description = models.TextField(null=True, blank=True, verbose_name='description')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='user')
    field = models.ForeignKey('Field', on_delete=models.PROTECT, verbose_name='field')

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ('field', 'user')

    def __str__(self):
        return str(self.raiting)


class Field(models.Model):
    address = models.CharField(max_length=254, verbose_name='address')
    latitude = models.FloatField(null=True, blank=True, verbose_name='latitude')
    longitude = models.FloatField(null=True, blank=True, verbose_name='longitude')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name='photo')
    contacts = models.TextField(blank=True, verbose_name='contacts')
    facilities = models.ManyToManyField('Facility', verbose_name='facilities')

    class Meta:
        verbose_name = 'поле'
        verbose_name_plural = 'поля'
        ordering = ('address',)
    
    def __str__(self):
        return self.address
    
    def calculate_rate(self):
        feedbacks = Feedback.objects.filter(field=self)
        
        summary = 0
        count = len(feedbacks)

        for i in range(count):
            summary += feedbacks[i].raiting

        return summary / count


class Facility(models.Model):
    name = models.CharField(max_length=50, verbose_name='name')
    icons_link = models.URLField(verbose_name='icons link')

    class Meta:
        verbose_name = 'удобство'
        verbose_name_plural = 'удобства'
        ordering = ('name',)

    def __str__(self):
        return self.name
