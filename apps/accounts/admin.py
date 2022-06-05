from django.contrib import admin
from .models import User, Telegram
from .verification.models import PhoneVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'first_name', 'last_name', 'email', 'birth_date')
    fields = (
        ('phone', 'password'),
        ('first_name', 'last_name'),
        ('date_joined', 'photo'),
        ('email', 'birth_date'),
        'groups', 'user_permissions'
    )

@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code')
    fields = list_display

@admin.register(Telegram)
class Telegram(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'age')
    fields = list_display
