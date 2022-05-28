from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name','phone')
    fields = (
        ('phone', 'password'),
        ('first_name', 'last_name'),
        ('username', 'photo'),
        ('email', 'birth_date'),
        'groups', 'user_permissions',
    )

@admin.register(models.Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code')
    fields = list_display
