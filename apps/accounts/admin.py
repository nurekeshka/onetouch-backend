from .verification.models import PhoneVerification
from django.contrib import admin
from .models import User


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
