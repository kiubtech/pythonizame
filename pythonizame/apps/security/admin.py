from django.contrib import admin
from .models import UserTokens


@admin.register(UserTokens)
class UserTokenRegistrationAdmin(admin.ModelAdmin):
    list_display = ('token', 'type', 'user', 'expiration_date', )
    list_filter = ('type', )
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
