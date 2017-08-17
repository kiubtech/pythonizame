from django.contrib import admin
from pythonizame.apps.account.models import UserProfile, Power, Achievement, UserAchievement
# Register your models here.


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'previous_image', 'num_available')
    list_display_links = ('id', 'name')
    search_fields = ['name']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('achievement', 'user', 'viewed', 'date_received')
    list_filter = ('achievement', )
    search_fields = ['user__username', 'user__first_name', 'achievement__name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    list_display = ('id', 'user')


@admin.register(Power)
class PowerAdmin(admin.ModelAdmin):
    list_display = ('name', 'python_auxiliary', 'status')
    list_filter = ('python_auxiliary', 'status')
