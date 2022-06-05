from .verification.models import PhoneVerification
from .models import User, Telegram
from django.contrib import admin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'first_name', 'last_name', 'email', 'birth_date')
    fields = (
        ('phone', 'password'),
        ('first_name', 'last_name'),
        ('date_joined', 'photo'),
        ('email', 'birth_date'),
        'groups', 'user_permissions',
        'telegram'
    )

@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code')
    fields = list_display

@admin.register(Telegram)
class TelegramAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'age')
    fields = list_display
