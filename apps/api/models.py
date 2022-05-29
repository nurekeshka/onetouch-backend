from django.db import models


class Photo(models.Model):
    link = models.URLField(null=True, blank=True, unique=True, verbose_name='link')

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'
        ordering = ('link',)

    def __str__(self):
        return self.link


