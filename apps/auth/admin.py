from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'first_name', 'last_name', 'email', 'birth_date')
    fields = (
        ('phone', 'password'),
        ('first_name', 'last_name'),
        ('date_joined', 'photo'),
        ('email', 'birth_date'),
        'groups', 'user_permissions'
    )

@admin.register(models.Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code')
    fields = list_display
